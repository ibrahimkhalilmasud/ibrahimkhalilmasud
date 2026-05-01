"""Rich-powered interactive CLI for the expense tracker."""
import sys
from datetime import date, datetime
from pathlib import Path
from typing import Optional

from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, FloatPrompt, IntPrompt, Prompt
from rich.table import Table
from rich.text import Text

from . import database as db
from .auto_categorizer import auto_categorize, list_categories
from .models import Budget, Expense
from .recurring import process_recurring
from .reports import ascii_bar_chart, export_to_csv, monthly_summary, spending_trend

console = Console()


# ── Helpers ──────────────────────────────────────────────────────────────────

def _header(title: str) -> None:
    console.print(Panel(f"[bold cyan]{title}[/bold cyan]", expand=False))


def _success(msg: str) -> None:
    console.print(f"[bold green]✔  {msg}[/bold green]")


def _error(msg: str) -> None:
    console.print(f"[bold red]✘  {msg}[/bold red]")


def _warn(msg: str) -> None:
    console.print(f"[bold yellow]⚠  {msg}[/bold yellow]")


def _ask_date(prompt: str = "Date (YYYY-MM-DD, blank = today)") -> date:
    while True:
        raw = Prompt.ask(prompt, default=date.today().isoformat())
        try:
            return date.fromisoformat(raw)
        except ValueError:
            _error("Invalid date format. Use YYYY-MM-DD.")


def _pick_category(suggested: str) -> str:
    cats = list_categories()
    console.print(f"\n[bold]Auto-suggested:[/bold] [cyan]{suggested}[/cyan]")
    console.print("\nCategories:")
    for i, cat in enumerate(cats, 1):
        marker = " ◄" if cat == suggested else ""
        console.print(f"  [dim]{i:2}.[/dim] {cat}{marker}")
    choice = Prompt.ask(
        "Pick a category number or press Enter to accept suggestion",
        default="",
    )
    if choice.strip() == "":
        return suggested
    try:
        idx = int(choice) - 1
        if 0 <= idx < len(cats):
            return cats[idx]
    except ValueError:
        pass
    _warn("Invalid choice – using suggested category.")
    return suggested


# ── Add expense ──────────────────────────────────────────────────────────────

def add_expense_ui() -> None:
    _header("Add Expense")
    description = Prompt.ask("Description")
    amount = FloatPrompt.ask("Amount ($)")
    exp_date = _ask_date()
    suggested = auto_categorize(description)
    category = _pick_category(suggested)

    is_recurring = Confirm.ask("Is this a recurring expense?", default=False)
    interval = None
    if is_recurring:
        interval = Prompt.ask(
            "Recurrence interval",
            choices=["daily", "weekly", "monthly"],
            default="monthly",
        )

    expense = Expense(
        amount=amount,
        description=description,
        category=category,
        date=exp_date,
        is_recurring=is_recurring,
        recurrence_interval=interval,
    )
    new_id = db.add_expense(expense)
    _success(f"Expense added (ID={new_id}): {category} – ${amount:.2f} on {exp_date}")


# ── List / filter expenses ───────────────────────────────────────────────────

def list_expenses_ui() -> None:
    _header("List Expenses")
    cats = ["(all)"] + list_categories()
    console.print("Filter by category:")
    for i, c in enumerate(cats, 1):
        console.print(f"  [dim]{i}.[/dim] {c}")
    cat_choice = Prompt.ask("Category number (Enter = all)", default="1")
    category: Optional[str] = None
    try:
        idx = int(cat_choice) - 1
        if idx > 0:
            category = cats[idx]
    except ValueError:
        pass

    start_raw = Prompt.ask("Start date (YYYY-MM-DD, blank = no limit)", default="")
    end_raw = Prompt.ask("End date   (YYYY-MM-DD, blank = today)", default=date.today().isoformat())

    start_date = date.fromisoformat(start_raw) if start_raw else None
    end_date = date.fromisoformat(end_raw) if end_raw else date.today()

    expenses = db.get_expenses(category=category, start_date=start_date, end_date=end_date)

    if not expenses:
        _warn("No expenses found for the given filters.")
        return

    table = Table(box=box.ROUNDED, title="Expenses", show_lines=True)
    table.add_column("ID", style="dim", justify="right")
    table.add_column("Date")
    table.add_column("Category", style="cyan")
    table.add_column("Description")
    table.add_column("Amount", style="green", justify="right")
    table.add_column("Recurring", justify="center")

    grand_total = 0.0
    for e in expenses:
        grand_total += e.amount
        rec_marker = "🔁" if e.is_recurring else ""
        table.add_row(
            str(e.id),
            str(e.date),
            e.category,
            e.description,
            f"${e.amount:,.2f}",
            rec_marker,
        )

    console.print(table)
    console.print(f"\n[bold]Total:[/bold] [green]${grand_total:,.2f}[/green] across {len(expenses)} expense(s)")


# ── Delete expense ───────────────────────────────────────────────────────────

def delete_expense_ui() -> None:
    _header("Delete Expense")
    expense_id = IntPrompt.ask("Enter Expense ID to delete")
    if Confirm.ask(f"Confirm delete expense ID={expense_id}?"):
        if db.delete_expense(expense_id):
            _success(f"Expense ID={expense_id} deleted.")
        else:
            _error(f"No expense found with ID={expense_id}.")


# ── Monthly report ───────────────────────────────────────────────────────────

def monthly_report_ui() -> None:
    _header("Monthly Report")
    today = date.today()
    year = IntPrompt.ask("Year", default=today.year)
    month = IntPrompt.ask("Month (1-12)", default=today.month)

    summary = monthly_summary(year, month)
    console.print(f"\n[bold]{summary['month_name']} {year}[/bold]\n")

    # Category breakdown
    table = Table(box=box.SIMPLE, title="Spending by Category")
    table.add_column("Category", style="cyan")
    table.add_column("Spent", justify="right", style="green")
    table.add_column("Budget Limit", justify="right")
    table.add_column("% Used", justify="right")

    for category, spent in summary["totals"].items():
        limit = summary["budgets"].get(category)
        pct_str = f"{(spent / limit * 100):.0f}%" if limit else "—"
        limit_str = f"${limit:,.2f}" if limit else "—"
        color = "red" if limit and spent > limit else "green"
        table.add_row(category, f"${spent:,.2f}", limit_str, f"[{color}]{pct_str}[/{color}]")

    console.print(table)
    console.print(f"\n[bold]Grand Total:[/bold] [green]${summary['grand_total']:,.2f}[/green]")

    # ASCII chart
    console.print("\n[bold]Spending Chart:[/bold]")
    console.print(ascii_bar_chart(summary["totals"]))

    # Alerts
    if summary["alerts"]:
        console.print()
        for alert in summary["alerts"]:
            if alert["status"] == "EXCEEDED":
                _error(f"Budget EXCEEDED: {alert['category']} – ${alert['spent']:,.2f} / ${alert['limit']:,.2f} ({alert['pct']:.0f}%)")
            else:
                _warn(f"Budget WARNING: {alert['category']} – ${alert['spent']:,.2f} / ${alert['limit']:,.2f} ({alert['pct']:.0f}%)")


# ── Spending trend ───────────────────────────────────────────────────────────

def spending_trend_ui() -> None:
    _header("Spending Trend (Last 6 Months)")
    trend = spending_trend(months=6)
    data = {f"{t['month_name'][:3]} {t['year']}": t["total"] for t in trend}
    console.print(ascii_bar_chart(data))
    console.print()


# ── Budget management ────────────────────────────────────────────────────────

def manage_budgets_ui() -> None:
    while True:
        _header("Budget Management")
        budgets = db.get_budgets()

        if budgets:
            table = Table(box=box.SIMPLE)
            table.add_column("Category", style="cyan")
            table.add_column("Monthly Limit", style="green", justify="right")
            for b in budgets:
                table.add_row(b.category, f"${b.monthly_limit:,.2f}")
            console.print(table)
        else:
            _warn("No budgets set yet.")

        console.print("\n[bold]Budget Options:[/bold]")
        console.print("  1. Set / update a budget")
        console.print("  2. Delete a budget")
        console.print("  3. Back")

        choice = Prompt.ask("Choice", choices=["1", "2", "3"], default="3")

        if choice == "1":
            cats = list_categories()
            for i, c in enumerate(cats, 1):
                console.print(f"  {i}. {c}")
            idx = IntPrompt.ask("Category number") - 1
            if 0 <= idx < len(cats):
                limit = FloatPrompt.ask(f"Monthly limit for {cats[idx]} ($)")
                db.set_budget(Budget(category=cats[idx], monthly_limit=limit))
                _success(f"Budget set: {cats[idx]} → ${limit:,.2f}/month")

        elif choice == "2":
            cat = Prompt.ask("Category name to remove budget")
            if db.delete_budget(cat):
                _success(f"Budget for '{cat}' removed.")
            else:
                _error(f"No budget found for '{cat}'.")

        else:
            break


# ── CSV export ───────────────────────────────────────────────────────────────

def export_csv_ui() -> None:
    _header("Export to CSV")
    filepath = Prompt.ask("Save file path", default="expenses_export.csv")
    start_raw = Prompt.ask("Start date (YYYY-MM-DD, blank = no limit)", default="")
    end_raw = Prompt.ask("End date   (YYYY-MM-DD, blank = today)", default=date.today().isoformat())
    start_date = date.fromisoformat(start_raw) if start_raw else None
    end_date = date.fromisoformat(end_raw) if end_raw else date.today()
    count = export_to_csv(filepath, start_date, end_date)
    _success(f"Exported {count} expense(s) to {filepath}")


# ── Main menu ────────────────────────────────────────────────────────────────

MENU = [
    ("Add Expense",          add_expense_ui),
    ("List / Filter Expenses", list_expenses_ui),
    ("Delete Expense",       delete_expense_ui),
    ("Monthly Report",       monthly_report_ui),
    ("Spending Trend",       spending_trend_ui),
    ("Manage Budgets",       manage_budgets_ui),
    ("Export to CSV",        export_csv_ui),
    ("Quit",                 None),
]


def run() -> None:
    db.initialize_db()

    # Auto-process recurring expenses
    created = process_recurring()
    if created:
        console.print(Panel(
            f"[bold green]Auto-added {len(created)} recurring expense(s)[/bold green]",
            expand=False,
        ))

    console.print(Panel(
        "[bold magenta]💰  Expense Tracker[/bold magenta]\n"
        "[dim]Track, categorize, and analyze your spending automatically.[/dim]",
        expand=False,
    ))

    while True:
        console.print("\n[bold]Main Menu:[/bold]")
        for i, (label, _) in enumerate(MENU, 1):
            console.print(f"  [dim]{i}.[/dim] {label}")

        choice = Prompt.ask(
            "Choose an option",
            choices=[str(i) for i in range(1, len(MENU) + 1)],
        )
        idx = int(choice) - 1
        label, handler = MENU[idx]

        if handler is None:
            console.print("[bold yellow]Goodbye! 👋[/bold yellow]")
            sys.exit(0)

        console.print()
        try:
            handler()
        except KeyboardInterrupt:
            console.print("\n[dim](cancelled)[/dim]")
        console.print()
