import unittest
from unittest.mock import MagicMock
from controller import ExpenseController

class TestExpenseController(unittest.TestCase):
    def setUp(self):
        """Set up mocks for model and view before each test."""
        self.mock_model = MagicMock()
        self.mock_view = MagicMock()
        
        self.controller = ExpenseController(self.mock_model)
        self.controller.set_view(self.mock_view)

    def test_add_expense_success(self):
        """Test successfully adding an expense."""
        # Setup mock view input data
        self.mock_view.get_input_data.return_value = {
            'date': '2023-10-27',
            'description': 'Test',
            'amount': '10.5'
        }
        
        self.controller.add_expense()
        
        # Assert model was called correctly
        self.mock_model.add_expense.assert_called_with('2023-10-27', 'Test', 10.5)
        # Assert view showed success
        self.mock_view.show_success.assert_called_once()
        self.mock_view.clear_inputs.assert_called_once()

    def test_add_expense_empty_fields(self):
        """Test adding expense with empty fields."""
        self.mock_view.get_input_data.return_value = {
            'date': '',
            'description': 'Test',
            'amount': '10.5'
        }
        
        self.controller.add_expense()
        
        self.mock_model.add_expense.assert_not_called()
        self.mock_view.show_error.assert_called_with("All fields are required.")

    def test_add_expense_invalid_amount(self):
        """Test adding expense with invalid amount (string)."""
        self.mock_view.get_input_data.return_value = {
            'date': '2023-10-27',
            'description': 'Test',
            'amount': 'abc'
        }
        
        self.controller.add_expense()
        
        self.mock_model.add_expense.assert_not_called()
        self.mock_view.show_error.assert_called_with("Amount must be a valid number.")

    def test_add_expense_negative_amount(self):
        """Test adding expense with negative amount."""
        self.mock_view.get_input_data.return_value = {
            'date': '2023-10-27',
            'description': 'Test',
            'amount': '-5.0'
        }
        
        self.controller.add_expense()
        
        self.mock_model.add_expense.assert_not_called()
        self.mock_view.show_error.assert_called_with("Amount cannot be negative.")

if __name__ == '__main__':
    unittest.main()
