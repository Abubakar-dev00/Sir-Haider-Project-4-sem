import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

class ExpenseView:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        
        # Configure root window
        self.root.title("Expense Tracker")
        self.root.geometry("500x600")
        self.root.configure(bg="#f4f4f9")
        
        # Apply modern font
        self.default_font = ("Inter", 11)
        self.title_font = ("Inter", 16, "bold")
        
        self.setup_ui()

    def setup_ui(self):
        """Set up the Tkinter user interface elements."""
        # Header
        header = tk.Label(self.root, text="Expense Tracker", font=self.title_font, bg="#f4f4f9", fg="#333333")
        header.pack(pady=15)
        
        # Input Frame
        input_frame = tk.Frame(self.root, bg="#f4f4f9")
        input_frame.pack(pady=10, padx=20, fill="x")
        
        # Date Input
        tk.Label(input_frame, text="Date (YYYY-MM-DD):", font=self.default_font, bg="#f4f4f9").grid(row=0, column=0, sticky="w", pady=5)
        self.date_entry = ttk.Entry(input_frame, font=self.default_font)
        self.date_entry.grid(row=0, column=1, sticky="ew", pady=5, padx=10)
        
        # Description Input
        tk.Label(input_frame, text="Description:", font=self.default_font, bg="#f4f4f9").grid(row=1, column=0, sticky="w", pady=5)
        self.desc_entry = ttk.Entry(input_frame, font=self.default_font)
        self.desc_entry.grid(row=1, column=1, sticky="ew", pady=5, padx=10)
        
        # Amount Input
        tk.Label(input_frame, text="Amount ($):", font=self.default_font, bg="#f4f4f9").grid(row=2, column=0, sticky="w", pady=5)
        self.amount_entry = ttk.Entry(input_frame, font=self.default_font)
        self.amount_entry.grid(row=2, column=1, sticky="ew", pady=5, padx=10)
        
        input_frame.columnconfigure(1, weight=1)
        
        # Add Button
        self.add_button = ttk.Button(self.root, text="Add Expense", command=self.controller.add_expense)
        self.add_button.pack(pady=10)
        
        # Listbox for displaying expenses
        list_frame = tk.Frame(self.root, bg="#f4f4f9")
        list_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        self.listbox = tk.Listbox(list_frame, font=("Courier", 10), selectbackground="#4CAF50")
        self.listbox.pack(side="left", fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.listbox.config(yscrollcommand=scrollbar.set)
        
        # Total Label
        self.total_label = tk.Label(self.root, text="Total: $0.00", font=self.title_font, bg="#f4f4f9", fg="#d32f2f")
        self.total_label.pack(pady=15)

    def get_input_data(self):
        """Retrieve data from input fields."""
        return {
            'date': self.date_entry.get().strip(),
            'description': self.desc_entry.get().strip(),
            'amount': self.amount_entry.get().strip()
        }

    def clear_inputs(self):
        """Clear all input fields."""
        self.date_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)

    def show_error(self, message):
        """Display an error message box."""
        messagebox.showerror("Error", message)

    def show_success(self, message):
        """Display a success message box."""
        messagebox.showinfo("Success", message)

    def update_expense_list(self, expenses):
        """Update the listbox with the provided expenses."""
        self.listbox.delete(0, tk.END)
        for expense in expenses:
            # Format: ID | Date | Description | Amount
            formatted_expense = f"{expense[1]:<12} | {expense[2]:<20} | ${expense[3]:>8.2f}"
            self.listbox.insert(tk.END, formatted_expense)

    def update_total(self, total):
        """Update the total expenses label."""
        self.total_label.config(text=f"Total: ${total:.2f}")
