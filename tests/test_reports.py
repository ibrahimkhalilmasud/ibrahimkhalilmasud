import csv
import tempfile
import unittest
from datetime import date
from pathlib import Path
from unittest.mock import patch

from expense_tracker.models import Expense
from expense_tracker.reports import ascii_bar_chart, export_to_csv


class ReportsTests(unittest.TestCase):
    def test_ascii_bar_chart_handles_empty_input(self) -> None:
        self.assertEqual(ascii_bar_chart({}), "  (no data)")

    def test_ascii_bar_chart_renders_small_non_zero_values(self) -> None:
        chart = ascii_bar_chart({"Small": 1, "Large": 100}, width=10)
        self.assertIn("Small", chart)
        self.assertIn("█", chart)

    @patch("expense_tracker.reports.db.get_expenses")
    def test_export_to_csv_creates_parent_directories(self, mock_get_expenses) -> None:
        mock_get_expenses.return_value = [
            Expense(
                id=1,
                amount=19.99,
                description="Lunch",
                category="Food & Dining",
                date=date(2026, 5, 1),
            )
        ]

        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "nested" / "exports" / "expenses.csv"
            count = export_to_csv(str(output_path))

            self.assertEqual(count, 1)
            self.assertTrue(output_path.exists())
            with output_path.open(newline="", encoding="utf-8") as file_obj:
                rows = list(csv.reader(file_obj))

        self.assertEqual(rows[0], ["ID", "Date", "Category", "Description", "Amount", "Recurring", "Interval"])
        self.assertEqual(rows[1][3], "Lunch")


if __name__ == "__main__":
    unittest.main()
