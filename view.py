import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import tkinter.filedialog as filedialog

class ExpenseView:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        
        # State variable for currently selected expense ID
        self.selected_expense_id = None
        
        # Configure root window
        self.root.title("Expense Tracker")
        self.root.geometry("600x700")
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
        
        # Category Input
        tk.Label(input_frame, text="Category:", font=self.default_font, bg="#f4f4f9").grid(row=1, column=0, sticky="w", pady=5)
        self.category_combobox = ttk.Combobox(input_frame, font=self.default_font, state="readonly", 
                                             values=['Food', 'Transport', 'Utilities', 'Entertainment', 'Other'])
        self.category_combobox.set('Other')
        self.category_combobox.grid(row=1, column=1, sticky="ew", pady=5, padx=10)

        # Description Input
        tk.Label(input_frame, text="Description:", font=self.default_font, bg="#f4f4f9").grid(row=2, column=0, sticky="w", pady=5)
        self.desc_entry = ttk.Entry(input_frame, font=self.default_font)
        self.desc_entry.grid(row=2, column=1, sticky="ew", pady=5, padx=10)
        
        # Amount Input
        tk.Label(input_frame, text="Amount ($):", font=self.default_font, bg="#f4f4f9").grid(row=3, column=0, sticky="w", pady=5)
        self.amount_entry = ttk.Entry(input_frame, font=self.default_font)
        self.amount_entry.grid(row=3, column=1, sticky="ew", pady=5, padx=10)
        
        input_frame.columnconfigure(1, weight=1)
        
        # Action Buttons Frame
        btn_frame = tk.Frame(self.root, bg="#f4f4f9")
        btn_frame.pack(pady=10)

        self.add_button = ttk.Button(btn_frame, text="Add", command=self.controller.add_expense)
        self.add_button.grid(row=0, column=0, padx=5)

        self.update_button = ttk.Button(btn_frame, text="Update", command=self.controller.update_expense)
        self.update_button.grid(row=0, column=1, padx=5)

        self.delete_button = ttk.Button(btn_frame, text="Delete", command=self.controller.delete_expense)
        self.delete_button.grid(row=0, column=2, padx=5)

        self.clear_button = ttk.Button(btn_frame, text="Clear", command=self.clear_inputs)
        self.clear_button.grid(row=0, column=3, padx=5)
        
        # Utilities Buttons Frame
        util_frame = tk.Frame(self.root, bg="#f4f4f9")
        util_frame.pack(pady=5)
        
        self.report_button = ttk.Button(util_frame, text="Monthly Report", command=self.controller.show_report)
        self.report_button.grid(row=0, column=0, padx=5)
        
        self.export_button = ttk.Button(util_frame, text="Export CSV", command=self.controller.export_csv)
        self.export_button.grid(row=0, column=1, padx=5)

        # Listbox for displaying expenses
        list_frame = tk.Frame(self.root, bg="#f4f4f9")
        list_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        self.listbox = tk.Listbox(list_frame, font=("Courier", 10), selectbackground="#4CAF50")
        self.listbox.pack(side="left", fill="both", expand=True)
        self.listbox.bind('<<ListboxSelect>>', self.on_listbox_select)
        
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.listbox.config(yscrollcommand=scrollbar.set)
        
        # Total Label
        self.total_label = tk.Label(self.root, text="Total: $0.00", font=self.title_font, bg="#f4f4f9", fg="#d32f2f")
        self.total_label.pack(pady=15)

    def on_listbox_select(self, event):
        """Handle selection in the listbox to populate input fields."""
        try:
            index = self.listbox.curselection()[0]
            expense_text = self.listbox.get(index)
            # Find the expense from controller
            expense_id = int(expense_text.split('|')[0].strip())
            self.controller.load_expense_to_inputs(expense_id)
        except IndexError:
            pass # Nothing selected

    def populate_inputs(self, expense_id, date, category, description, amount):
        """Populate the input fields with specific expense data."""
        self.selected_expense_id = expense_id
        
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, date)
        
        self.category_combobox.set(category)
        
        self.desc_entry.delete(0, tk.END)
        self.desc_entry.insert(0, description)
        
        self.amount_entry.delete(0, tk.END)
        self.amount_entry.insert(0, str(amount))

    def get_input_data(self):
        """Retrieve data from input fields."""
        return {
            'date': self.date_entry.get().strip(),
            'category': self.category_combobox.get().strip(),
            'description': self.desc_entry.get().strip(),
            'amount': self.amount_entry.get().strip()
        }

    def clear_inputs(self):
        """Clear all input fields and reset selection."""
        self.selected_expense_id = None
        self.date_entry.delete(0, tk.END)
        self.category_combobox.set('Other')
        self.desc_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
        self.listbox.selection_clear(0, tk.END)

    def show_error(self, message):
        """Display an error message box."""
        messagebox.showerror("Error", message)

    def show_success(self, message):
        """Display a success message box."""
        messagebox.showinfo("Success", message)

    def ask_yes_no(self, title, message):
        """Ask a yes/no question."""
        return messagebox.askyesno(title, message)

    def ask_save_file(self):
        """Open a file dialog to save a CSV."""
        return filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])

    def update_expense_list(self, expenses):
        """Update the listbox with the provided expenses."""
        self.listbox.delete(0, tk.END)
        for expense in expenses:
            # Format: ID | Date | Category | Description | Amount
            formatted_expense = f"{expense[0]:<4} | {expense[1]:<10} | {expense[4]:<13} | {expense[2]:<15} | ${expense[3]:>8.2f}"
            self.listbox.insert(tk.END, formatted_expense)

    def update_total(self, total):
        """Update the total expenses label."""
        self.total_label.config(text=f"Total: ${total:.2f}")

    def show_monthly_report_window(self, report_data):
        """Open a new window displaying the monthly report."""
        report_win = tk.Toplevel(self.root)
        report_win.title("Monthly Report")
        report_win.geometry("400x300")
        
        tk.Label(report_win, text="Monthly Report by Category", font=self.title_font).pack(pady=10)
        
        list_frame = tk.Frame(report_win)
        list_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        report_listbox = tk.Listbox(list_frame, font=("Courier", 10))
        report_listbox.pack(side="left", fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=report_listbox.yview)
        scrollbar.pack(side="right", fill="y")
        report_listbox.config(yscrollcommand=scrollbar.set)
        
        for row in report_data:
            month = row[0]
            category = row[1]
            total = row[2]
            report_listbox.insert(tk.END, f"{month} | {category:<13} | ${total:.2f}")
