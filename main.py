import tkinter as tk
from model import ExpenseModel
from view import ExpenseView
from controller import ExpenseController

def main():
    # Initialize Model
    model = ExpenseModel(db_name="expenses_refactored.db")
    
    # Initialize Controller with Model
    controller = ExpenseController(model)
    
    # Initialize Tkinter Root
    root = tk.Tk()
    
    # Initialize View with Root and Controller
    view = ExpenseView(root, controller)
    
    # Inject View into Controller
    controller.set_view(view)
    
    # Handle window close event to ensure DB connection is closed
    def on_closing():
        model.close()
        root.destroy()
        
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    # Start GUI loop
    root.mainloop()

if __name__ == "__main__":
    main()
