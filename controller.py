class ExpenseController:
    def __init__(self, model):
        self.model = model
        self.view = None # Will be injected later

    def set_view(self, view):
        self.view = view
        self.refresh_data()

    def add_expense(self):
        """Handle the action of adding a new expense."""
        data = self.view.get_input_data()
        
        date = data['date']
        description = data['description']
        amount_str = data['amount']
        
        # Validation and Exception Handling
        if not date or not description or not amount_str:
            self.view.show_error("All fields are required.")
            return
            
        try:
            amount = float(amount_str)
            if amount < 0:
                self.view.show_error("Amount cannot be negative.")
                return
        except ValueError:
            self.view.show_error("Amount must be a valid number.")
            return
            
        try:
            self.model.add_expense(date, description, amount)
            self.view.show_success("Expense added successfully.")
            self.view.clear_inputs()
            self.refresh_data()
        except Exception as e:
            self.view.show_error(str(e))

    def refresh_data(self):
        """Fetch updated data from the model and update the view."""
        try:
            expenses = self.model.get_all_expenses()
            self.view.update_expense_list(expenses)
            
            total = self.model.get_total_expenses()
            self.view.update_total(total)
        except Exception as e:
            self.view.show_error(str(e))
