import unittest
import os
from model import ExpenseModel

class TestExpenseModel(unittest.TestCase):
    def setUp(self):
        """Set up a temporary database for testing."""
        self.test_db = "test_expenses.db"
        self.model = ExpenseModel(db_name=self.test_db)

    def tearDown(self):
        """Clean up the temporary database after each test."""
        self.model.close()
        if os.path.exists(self.test_db):
            os.remove(self.test_db)

    def test_add_expense(self):
        """Test adding an expense to the database."""
        self.model.add_expense("2023-10-27", "Groceries", 50.50)
        expenses = self.model.get_all_expenses()
        self.assertEqual(len(expenses), 1)
        self.assertEqual(expenses[0][1], "2023-10-27")
        self.assertEqual(expenses[0][2], "Groceries")
        self.assertEqual(expenses[0][3], 50.50)

    def test_get_total_expenses(self):
        """Test calculating the total of all expenses."""
        self.model.add_expense("2023-10-27", "Groceries", 50.00)
        self.model.add_expense("2023-10-28", "Gas", 30.00)
        total = self.model.get_total_expenses()
        self.assertEqual(total, 80.00)

    def test_get_total_empty_db(self):
        """Test total when database is empty."""
        total = self.model.get_total_expenses()
        self.assertEqual(total, 0.0)

if __name__ == '__main__':
    unittest.main()
