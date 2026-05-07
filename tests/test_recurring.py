import unittest
from datetime import date
from unittest.mock import patch

from expense_tracker.models import Expense
from expense_tracker.recurring import _next_due, process_recurring


class NextDueTests(unittest.TestCase):
    def test_daily_rolls_into_next_month(self) -> None:
        self.assertEqual(_next_due(date(2026, 1, 31), "daily"), date(2026, 2, 1))

    def test_weekly_adds_seven_days(self) -> None:
        self.assertEqual(_next_due(date(2026, 5, 1), "weekly"), date(2026, 5, 8))

    def test_monthly_clamps_to_last_day(self) -> None:
        self.assertEqual(_next_due(date(2026, 1, 31), "monthly"), date(2026, 2, 28))


class ProcessRecurringTests(unittest.TestCase):
    @patch("expense_tracker.recurring.db.set_last_run")
    @patch("expense_tracker.recurring.db.add_expense")
    @patch("expense_tracker.recurring.db.get_last_run")
    @patch("expense_tracker.recurring.db.get_recurring_expenses")
    def test_creates_due_expense_copy(
        self,
        mock_get_recurring_expenses,
        mock_get_last_run,
        mock_add_expense,
        mock_set_last_run,
    ) -> None:
        template = Expense(
            id=10,
            amount=15.0,
            description="Gym membership",
            category="Health",
            date=date(2026, 4, 1),
            is_recurring=True,
            recurrence_interval="monthly",
        )
        mock_get_recurring_expenses.return_value = [template]
        mock_get_last_run.return_value = date(2026, 4, 1)

        created = process_recurring(today=date(2026, 5, 2))

        self.assertEqual(len(created), 1)
        self.assertEqual(created[0].description, "[Auto] Gym membership")
        self.assertEqual(created[0].date, date(2026, 5, 2))
        mock_add_expense.assert_called_once()
        mock_set_last_run.assert_called_once_with(10, date(2026, 5, 2))


if __name__ == "__main__":
    unittest.main()
