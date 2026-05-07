import unittest

from expense_tracker.auto_categorizer import DEFAULT_CATEGORY, auto_categorize, list_categories


class AutoCategorizerTests(unittest.TestCase):
    def test_matches_known_keyword_case_insensitively(self) -> None:
        self.assertEqual(auto_categorize("NETFLIX family plan"), "Entertainment")

    def test_returns_default_for_unknown_description(self) -> None:
        self.assertEqual(auto_categorize("miscellaneous payment"), DEFAULT_CATEGORY)

    def test_lists_default_category(self) -> None:
        self.assertIn(DEFAULT_CATEGORY, list_categories())


if __name__ == "__main__":
    unittest.main()
