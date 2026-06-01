import csv

class ExpenseController:
    def __init__(self, model):
        self.model = model
        self.view = None

    def set_view(self, view):
        self.view = view
        self.refresh_data()

    def add_expense(self):
        """Handle adding a new expense."""
        data = self.view.get_input_data()
        
        date = data['date']
        category = data['category']
        description = data['description']
        amount_str = data['amount']
        
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
            self.model.add_expense(date, category, description, amount)
            self.view.show_success("Expense added successfully.")
            self.view.clear_inputs()
            self.refresh_data()
        except Exception as e:
            self.view.show_error(str(e))

    def update_expense(self):
        """Handle updating an existing expense."""
        if self.view.selected_expense_id is None:
            self.view.show_error("Please select an expense to update.")
            return

        data = self.view.get_input_data()
        
        date = data['date']
        category = data['category']
        description = data['description']
        amount_str = data['amount']
        
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
            self.model.update_expense(self.view.selected_expense_id, date, category, description, amount)
            self.view.show_success("Expense updated successfully.")
            self.view.clear_inputs()
            self.refresh_data()
        except Exception as e:
            self.view.show_error(str(e))

    def delete_expense(self):
        """Handle deleting an expense."""
        if self.view.selected_expense_id is None:
            self.view.show_error("Please select an expense to delete.")
            return

        if self.view.ask_yes_no("Confirm Delete", "Are you sure you want to delete this expense?"):
            try:
                self.model.delete_expense(self.view.selected_expense_id)
                self.view.show_success("Expense deleted successfully.")
                self.view.clear_inputs()
                self.refresh_data()
            except Exception as e:
                self.view.show_error(str(e))

    def load_expense_to_inputs(self, expense_id):
        """Load specific expense data into the view's inputs."""
        try:
            expenses = self.model.get_all_expenses()
            for exp in expenses:
                if exp[0] == expense_id:
                    self.view.populate_inputs(exp[0], exp[1], exp[4], exp[2], exp[3])
                    break
        except Exception as e:
            self.view.show_error(str(e))

    def show_report(self):
        """Show the monthly report window."""
        try:
            report_data = self.model.get_monthly_report()
            self.view.show_monthly_report_window(report_data)
        except Exception as e:
            self.view.show_error(str(e))

    def export_csv(self):
        """Export all expenses to a CSV file."""
        filepath = self.view.ask_save_file()
        if not filepath:
            return # User cancelled

        try:
            expenses = self.model.get_all_expenses()
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['ID', 'Date', 'Description', 'Amount', 'Category'])
                for exp in expenses:
                    writer.writerow(exp)
            self.view.show_success("Data exported successfully.")
        except Exception as e:
            self.view.show_error(f"Error exporting data: {str(e)}")

    def refresh_data(self):
        """Fetch updated data from the model and update the view."""
        try:
            expenses = self.model.get_all_expenses()
            self.view.update_expense_list(expenses)
            
            total = self.model.get_total_expenses()
            self.view.update_total(total)
        except Exception as e:
            self.view.show_error(str(e))
