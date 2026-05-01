"""SQLite database layer for the expense tracker."""
import sqlite3
from contextlib import contextmanager
from datetime import date, timedelta
from pathlib import Path
from typing import Generator, Optional

from .models import Budget, Expense

DB_PATH = Path.home() / ".expense_tracker" / "expenses.db"


def _ensure_db_dir() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)


@contextmanager
def _connect() -> Generator[sqlite3.Connection, None, None]:
    _ensure_db_dir()
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def initialize_db() -> None:
    """Create tables if they don't exist."""
    with _connect() as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS expenses (
                id                  INTEGER PRIMARY KEY AUTOINCREMENT,
                amount              REAL    NOT NULL,
                description         TEXT    NOT NULL,
                category            TEXT    NOT NULL,
                date                TEXT    NOT NULL,
                is_recurring        INTEGER NOT NULL DEFAULT 0,
                recurrence_interval TEXT
            );

            CREATE TABLE IF NOT EXISTS budgets (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                category      TEXT    NOT NULL UNIQUE,
                monthly_limit REAL    NOT NULL
            );

            CREATE TABLE IF NOT EXISTS recurring_log (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                expense_id INTEGER NOT NULL REFERENCES expenses(id) ON DELETE CASCADE,
                last_run   TEXT    NOT NULL
            );

            CREATE UNIQUE INDEX IF NOT EXISTS idx_recurring_log_expense_id
                ON recurring_log(expense_id);
            """
        )


# ── Expenses ────────────────────────────────────────────────────────────────

def add_expense(expense: Expense) -> int:
    """Insert a new expense and return its id."""
    with _connect() as conn:
        cursor = conn.execute(
            """
            INSERT INTO expenses (amount, description, category, date,
                                  is_recurring, recurrence_interval)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                expense.amount,
                expense.description,
                expense.category,
                expense.date.isoformat(),
                int(expense.is_recurring),
                expense.recurrence_interval,
            ),
        )
        return cursor.lastrowid  # type: ignore[return-value]


def get_expenses(
    *,
    category: Optional[str] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    limit: Optional[int] = None,
) -> list[Expense]:
    query = "SELECT * FROM expenses WHERE 1=1"
    params: list = []
    if category:
        query += " AND category = ?"
        params.append(category)
    if start_date:
        query += " AND date >= ?"
        params.append(start_date.isoformat())
    if end_date:
        query += " AND date <= ?"
        params.append(end_date.isoformat())
    query += " ORDER BY date DESC, id DESC"
    if limit:
        query += " LIMIT ?"
        params.append(limit)

    with _connect() as conn:
        rows = conn.execute(query, params).fetchall()
    return [_row_to_expense(r) for r in rows]


def delete_expense(expense_id: int) -> bool:
    with _connect() as conn:
        cursor = conn.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
        return cursor.rowcount > 0


def update_expense(expense: Expense) -> bool:
    with _connect() as conn:
        cursor = conn.execute(
            """
            UPDATE expenses
               SET amount=?, description=?, category=?, date=?,
                   is_recurring=?, recurrence_interval=?
             WHERE id=?
            """,
            (
                expense.amount,
                expense.description,
                expense.category,
                expense.date.isoformat(),
                int(expense.is_recurring),
                expense.recurrence_interval,
                expense.id,
            ),
        )
        return cursor.rowcount > 0


def _row_to_expense(row: sqlite3.Row) -> Expense:
    return Expense(
        id=row["id"],
        amount=row["amount"],
        description=row["description"],
        category=row["category"],
        date=date.fromisoformat(row["date"]),
        is_recurring=bool(row["is_recurring"]),
        recurrence_interval=row["recurrence_interval"],
    )


# ── Budgets ─────────────────────────────────────────────────────────────────

def set_budget(budget: Budget) -> None:
    with _connect() as conn:
        conn.execute(
            """
            INSERT INTO budgets (category, monthly_limit)
            VALUES (?, ?)
            ON CONFLICT(category) DO UPDATE SET monthly_limit=excluded.monthly_limit
            """,
            (budget.category, budget.monthly_limit),
        )


def get_budgets() -> list[Budget]:
    with _connect() as conn:
        rows = conn.execute("SELECT * FROM budgets ORDER BY category").fetchall()
    return [Budget(id=r["id"], category=r["category"], monthly_limit=r["monthly_limit"]) for r in rows]


def delete_budget(category: str) -> bool:
    with _connect() as conn:
        cursor = conn.execute("DELETE FROM budgets WHERE category = ?", (category,))
        return cursor.rowcount > 0


# ── Recurring log ────────────────────────────────────────────────────────────

def get_recurring_expenses() -> list[Expense]:
    with _connect() as conn:
        rows = conn.execute(
            "SELECT * FROM expenses WHERE is_recurring = 1"
        ).fetchall()
    return [_row_to_expense(r) for r in rows]


def get_last_run(expense_id: int) -> Optional[date]:
    with _connect() as conn:
        row = conn.execute(
            "SELECT last_run FROM recurring_log WHERE expense_id = ?", (expense_id,)
        ).fetchone()
    return date.fromisoformat(row["last_run"]) if row else None


def set_last_run(expense_id: int, run_date: date) -> None:
    with _connect() as conn:
        conn.execute(
            """
            INSERT INTO recurring_log (expense_id, last_run) VALUES (?, ?)
            ON CONFLICT(expense_id) DO UPDATE SET last_run=excluded.last_run
            """,
            (expense_id, run_date.isoformat()),
        )


# ── Summary helpers ──────────────────────────────────────────────────────────

def monthly_totals_by_category(year: int, month: int) -> dict[str, float]:
    """Return {category: total_spent} for the given month."""
    start = date(year, month, 1)
    # last day of month
    if month == 12:
        end = date(year + 1, 1, 1) - timedelta(days=1)
    else:
        end = date(year, month + 1, 1) - timedelta(days=1)

    with _connect() as conn:
        rows = conn.execute(
            """
            SELECT category, SUM(amount) as total
              FROM expenses
             WHERE date >= ? AND date <= ?
             GROUP BY category
             ORDER BY total DESC
            """,
            (start.isoformat(), end.isoformat()),
        ).fetchall()
    return {r["category"]: r["total"] for r in rows}


def total_spent(start_date: date, end_date: date) -> float:
    with _connect() as conn:
        row = conn.execute(
            "SELECT COALESCE(SUM(amount), 0) as total FROM expenses WHERE date >= ? AND date <= ?",
            (start_date.isoformat(), end_date.isoformat()),
        ).fetchone()
    return row["total"]
