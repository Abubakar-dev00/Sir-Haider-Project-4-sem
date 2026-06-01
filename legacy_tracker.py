import tkinter as tk
from tkinter import messagebox
import sqlite3

# Global variable for DB connection
conn = sqlite3.connect('expenses_legacy.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS expenses
                  (id INTEGER PRIMARY KEY, date TEXT, description TEXT, amount REAL)''')
conn.commit()

def add_expense():
    # Direct database interaction inside GUI logic, poor exception handling
    d = date_entry.get()
    desc = desc_entry.get()
    amt = amount_entry.get()
    
    if d == "" or desc == "" or amt == "":
        messagebox.showerror("Error", "All fields required")
        return
        
    try:
        amt = float(amt)
    except:
        messagebox.showerror("Error", "Amount must be a number")
        return
        
    cursor.execute("INSERT INTO expenses (date, description, amount) VALUES (?, ?, ?)", (d, desc, amt))
    conn.commit()
    messagebox.showinfo("Success", "Expense Added")
    refresh_list()

def refresh_list():
    listbox.delete(0, tk.END)
    cursor.execute("SELECT * FROM expenses")
    rows = cursor.fetchall()
    total = 0
    for row in rows:
        listbox.insert(tk.END, f"{row[1]} | {row[2]} | ${row[3]}")
        total += row[3]
    total_label.config(text=f"Total: ${total:.2f}")

# Monolithic GUI Setup
root = tk.Tk()
root.title("Legacy Expense Tracker")
root.geometry("400x500")

tk.Label(root, text="Date (YYYY-MM-DD)").pack()
date_entry = tk.Entry(root)
date_entry.pack()

tk.Label(root, text="Description").pack()
desc_entry = tk.Entry(root)
desc_entry.pack()

tk.Label(root, text="Amount ($)").pack()
amount_entry = tk.Entry(root)
amount_entry.pack()

tk.Button(root, text="Add Expense", command=add_expense).pack(pady=10)

listbox = tk.Listbox(root, width=50, height=15)
listbox.pack(pady=10)

total_label = tk.Label(root, text="Total: $0.00", font=("Helvetica", 14, "bold"))
total_label.pack()

refresh_list()

# Running directly without if __name__ == "__main__"
root.mainloop()
