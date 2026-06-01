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
                                   (id INTEGER PRIMARY KEY, date TEXT, description TEXT, amount REAL)''')
            self.conn.commit()
        except sqlite3.Error as e:
            raise Exception(f"Database Initialization Error: {e}")

    def add_expense(self, date: str, description: str, amount: float):
        """Add a new expense to the database."""
        try:
            self.cursor.execute("INSERT INTO expenses (date, description, amount) VALUES (?, ?, ?)",
                                (date, description, amount))
            self.conn.commit()
        except sqlite3.Error as e:
            raise Exception(f"Database Error while adding expense: {e}")

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

    def close(self):
        """Close the database connection."""
        if self.conn:
            self.conn.close()
