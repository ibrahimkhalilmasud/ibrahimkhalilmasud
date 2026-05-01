"""Auto-process recurring expenses on application startup."""
import calendar
from datetime import date

from . import database as db
from .models import Expense


def _next_due(last_run: date, interval: str) -> date:
    """Return the date when the next recurrence is due."""
    if interval == "daily":
        return date(last_run.year, last_run.month, last_run.day + 1
                    ) if last_run.day < calendar.monthrange(last_run.year, last_run.month)[1] \
               else date(last_run.year, last_run.month, last_run.day).__class__.fromordinal(
                   last_run.toordinal() + 1)
    if interval == "weekly":
        return date.fromordinal(last_run.toordinal() + 7)
    # monthly: same day next month (clamped to last day of that month)
    total_months = last_run.year * 12 + last_run.month  # 0-indexed month after increment
    year = total_months // 12
    month = total_months % 12 + 1
    max_day = calendar.monthrange(year, month)[1]
    return date(year, month, min(last_run.day, max_day))


def process_recurring(today: date | None = None) -> list[Expense]:
    """
    Check all recurring expenses and add a new entry for each one
    that is due today or overdue.  Returns the list of newly-created copies.
    """
    if today is None:
        today = date.today()

    created: list[Expense] = []
    for template in db.get_recurring_expenses():
        interval = template.recurrence_interval or "monthly"

        last_run = db.get_last_run(template.id)  # type: ignore[arg-type]
        if last_run is None:
            due = today  # first run – treat as due immediately
        else:
            due = _next_due(last_run, interval)

        if today >= due:
            new_expense = Expense(
                amount=template.amount,
                description=f"[Auto] {template.description}",
                category=template.category,
                date=today,
                is_recurring=False,  # copy is a regular expense
            )
            db.add_expense(new_expense)
            db.set_last_run(template.id, today)  # type: ignore[arg-type]
            created.append(new_expense)

    return created
