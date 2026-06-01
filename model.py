import sqlite3

class ExpenseModel:
    def __init__(self, db_name="expenses.db"):
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self._initialize_db()

    def _initialize_db(self):
        """Initialize the database and create table if it doesn't exist."""
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS expenses
                                   (id INTEGER PRIMARY KEY, date TEXT, description TEXT, amount REAL, category TEXT DEFAULT 'Other')''')
            
            # Database Migration: Attempt to add category column if it doesn't exist (for existing databases)
            try:
                self.cursor.execute("ALTER TABLE expenses ADD COLUMN category TEXT DEFAULT 'Other'")
            except sqlite3.OperationalError:
                pass # Column already exists
                
            self.conn.commit()
        except sqlite3.Error as e:
            raise Exception(f"Database Initialization Error: {e}")

    def add_expense(self, date: str, category: str, description: str, amount: float):
        """Add a new expense to the database."""
        try:
            self.cursor.execute("INSERT INTO expenses (date, category, description, amount) VALUES (?, ?, ?, ?)",
                                (date, category, description, amount))
            self.conn.commit()
        except sqlite3.Error as e:
            raise Exception(f"Database Error while adding expense: {e}")

    def update_expense(self, expense_id: int, date: str, category: str, description: str, amount: float):
        """Update an existing expense."""
        try:
            self.cursor.execute("UPDATE expenses SET date=?, category=?, description=?, amount=? WHERE id=?",
                                (date, category, description, amount, expense_id))
            self.conn.commit()
        except sqlite3.Error as e:
            raise Exception(f"Database Error while updating expense: {e}")

    def delete_expense(self, expense_id: int):
        """Delete an expense from the database."""
        try:
            self.cursor.execute("DELETE FROM expenses WHERE id=?", (expense_id,))
            self.conn.commit()
        except sqlite3.Error as e:
            raise Exception(f"Database Error while deleting expense: {e}")

    def get_all_expenses(self):
        """Retrieve all expenses from the database."""
        try:
            self.cursor.execute("SELECT * FROM expenses")
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            raise Exception(f"Database Error while retrieving expenses: {e}")

    def get_total_expenses(self):
        """Calculate the total of all expenses."""
        try:
            self.cursor.execute("SELECT SUM(amount) FROM expenses")
            result = self.cursor.fetchone()
            return result[0] if result[0] is not None else 0.0
        except sqlite3.Error as e:
            raise Exception(f"Database Error while calculating total: {e}")

    def get_monthly_report(self):
        """Aggregate expenses by year-month and category."""
        try:
            # Groups by YYYY-MM and category
            self.cursor.execute("""
                SELECT strftime('%Y-%m', date) as month, category, SUM(amount) 
                FROM expenses 
                GROUP BY month, category
                ORDER BY month DESC
            """)
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            raise Exception(f"Database Error while generating report: {e}")

    def close(self):
        """Close the database connection."""
        if self.conn:
            self.conn.close()
