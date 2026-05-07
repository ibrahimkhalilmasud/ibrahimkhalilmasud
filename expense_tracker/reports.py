"""Reports, summaries, budget alerts and CSV export."""
import calendar
import csv
from datetime import date
from pathlib import Path
from typing import Optional

from . import database as db


# ── Monthly summary ──────────────────────────────────────────────────────────

def monthly_summary(year: int, month: int) -> dict:
    """Return a dict with category totals, grand total, and budget alerts."""
    totals = db.monthly_totals_by_category(year, month)
    grand_total = sum(totals.values())
    budgets = {b.category: b.monthly_limit for b in db.get_budgets()}

    alerts = []
    for category, spent in totals.items():
        limit = budgets.get(category)
        if limit:
            pct = (spent / limit) * 100
            if pct >= 100:
                alerts.append(
                    {"category": category, "spent": spent, "limit": limit, "pct": pct, "status": "EXCEEDED"}
                )
            elif pct >= 80:
                alerts.append(
                    {"category": category, "spent": spent, "limit": limit, "pct": pct, "status": "WARNING"}
                )

    return {
        "year": year,
        "month": month,
        "month_name": calendar.month_name[month],
        "totals": totals,
        "grand_total": grand_total,
        "budgets": budgets,
        "alerts": alerts,
    }


# ── Spending trend (last N months) ──────────────────────────────────────────

def spending_trend(months: int = 6) -> list[dict]:
    """Return total spending per month for the last `months` months."""
    today = date.today()
    result = []
    for i in range(months - 1, -1, -1):
        # Subtract i months from the current month using proper calendar arithmetic
        total_months = today.year * 12 + (today.month - 1) - i
        year = total_months // 12
        month = total_months % 12 + 1
        first_day = date(year, month, 1)
        last_day_num = calendar.monthrange(year, month)[1]
        last_day = date(year, month, last_day_num)
        total = db.total_spent(first_day, last_day)
        result.append({"year": year, "month": month, "month_name": calendar.month_name[month], "total": total})
    return result


# ── ASCII bar chart ──────────────────────────────────────────────────────────

def ascii_bar_chart(data: dict[str, float], width: int = 30) -> str:
    """Render a simple horizontal bar chart as a string."""
    if not data:
        return "  (no data)"
    max_val = max(data.values()) or 1
    lines = []
    for label, value in data.items():
        bar_len = 0 if value <= 0 else max(1, int((value / max_val) * width))
        bar = "█" * bar_len
        lines.append(f"  {label:<25} {bar} ${value:,.2f}")
    return "\n".join(lines)


# ── CSV export ───────────────────────────────────────────────────────────────

def export_to_csv(
    filepath: str,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
) -> int:
    """Export expenses to a CSV file. Returns the number of rows written."""
    expenses = db.get_expenses(start_date=start_date, end_date=end_date)
    export_path = Path(filepath).expanduser()
    export_path.parent.mkdir(parents=True, exist_ok=True)
    with export_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "Date", "Category", "Description", "Amount", "Recurring", "Interval"])
        for e in expenses:
            writer.writerow([
                e.id, e.date.isoformat(), e.category, e.description,
                f"{e.amount:.2f}", "Yes" if e.is_recurring else "No",
                e.recurrence_interval or "",
            ])
    return len(expenses)
