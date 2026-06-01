import base64
import urllib.request
import re
import os

def generate_image(mermaid_code, filename):
    try:
        # Encode mermaid code to base64
        encoded = base64.b64encode(mermaid_code.encode('utf-8')).decode('utf-8')
        url = f"https://mermaid.ink/img/{encoded}"
        
        # Add a custom User-Agent to avoid HTTP 403 Forbidden
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        
        with urllib.request.urlopen(req) as response:
            with open(filename, 'wb') as f:
                f.write(response.read())
        print(f"Successfully generated {filename}")
    except Exception as e:
        print(f"Failed to generate {filename}: {e}")

# Extracted mermaid blocks from uml_diagrams.md
diagrams = {
    "01_architecture_class_diagram.png": """classDiagram
    class ExpenseModel {
        -db_name : str
        -conn : sqlite3.Connection
        -cursor : sqlite3.Cursor
        +__init__(db_name)
        -_initialize_db()
        +add_expense(date, category, description, amount)
        +update_expense(expense_id, date, category, description, amount)
        +delete_expense(expense_id)
        +get_all_expenses() : list
        +get_total_expenses() : float
        +get_monthly_report() : list
        +close()
    }

    class ExpenseView {
        -root : tk.Tk
        -controller : ExpenseController
        -selected_expense_id : int
        +get_input_data() : dict
        +populate_inputs(...)
        +clear_inputs()
        +update_expense_list(expenses)
        +update_total(total)
        +show_error(message)
        +show_success(message)
        +ask_yes_no(title, message) : bool
        +ask_save_file() : str
        +show_monthly_report_window(report_data)
    }

    class ExpenseController {
        -model : ExpenseModel
        -view : ExpenseView
        +add_expense()
        +update_expense()
        +delete_expense()
        +load_expense_to_inputs(expense_id)
        +show_report()
        +export_csv()
        +refresh_data()
    }

    ExpenseController --> ExpenseModel : Manipulates Data
    ExpenseController --> ExpenseView : Updates UI
    ExpenseView --> ExpenseController : Triggers Events""",

    "02_add_expense_sequence.png": """sequenceDiagram
    actor User
    participant View as ExpenseView
    participant Controller as ExpenseController
    participant Model as ExpenseModel

    User->>View: Enters Data & Clicks "Add"
    View->>Controller: add_expense()
    
    activate Controller
    Controller->>View: get_input_data()
    View-->>Controller: Returns {date, category, desc, amount}
    
    Note over Controller: Validates Input
    
    alt Invalid Input
        Controller->>View: show_error("Invalid amount")
    else Valid Input
        Controller->>Model: add_expense(date, category, desc, amount)
        activate Model
        Model-->>Controller: Success (or Exception caught)
        deactivate Model
        
        Controller->>View: show_success("Added successfully")
        Controller->>Controller: refresh_data()
    end
    deactivate Controller""",

    "03_update_expense_sequence.png": """sequenceDiagram
    actor User
    participant View as ExpenseView
    participant Controller as ExpenseController
    participant Model as ExpenseModel

    User->>View: Selects Expense from Listbox
    View->>Controller: load_expense_to_inputs(expense_id)
    Controller->>Model: get_all_expenses()
    Model-->>Controller: Returns expenses list
    Controller->>View: populate_inputs(...)
    
    User->>View: Modifies Data & Clicks "Update"
    View->>Controller: update_expense()
    
    activate Controller
    Controller->>View: get_input_data()
    View-->>Controller: Returns modified {date, category, desc, amount}
    
    Note over Controller: Validates Input
    
    Controller->>Model: update_expense(expense_id, ...)
    activate Model
    Model-->>Controller: Success
    deactivate Model
    
    Controller->>View: show_success("Updated successfully")
    Controller->>Controller: refresh_data()
    deactivate Controller""",

    "04_delete_expense_sequence.png": """sequenceDiagram
    actor User
    participant View as ExpenseView
    participant Controller as ExpenseController
    participant Model as ExpenseModel

    User->>View: Selects Expense & Clicks "Delete"
    View->>Controller: delete_expense()
    
    activate Controller
    Controller->>View: ask_yes_no("Confirm Delete")
    View-->>User: Shows Confirmation Dialog
    User-->>View: Clicks "Yes"
    View-->>Controller: Returns True
    
    Controller->>Model: delete_expense(expense_id)
    activate Model
    Model-->>Controller: Success
    deactivate Model
    
    Controller->>View: show_success("Deleted successfully")
    Controller->>Controller: refresh_data()
    deactivate Controller""",

    "05_monthly_report_sequence.png": """sequenceDiagram
    actor User
    participant View as ExpenseView
    participant Controller as ExpenseController
    participant Model as ExpenseModel
    participant DB as SQLite DB

    User->>View: Clicks "Monthly Report"
    View->>Controller: show_report()
    
    activate Controller
    Controller->>Model: get_monthly_report()
    activate Model
    
    Model->>DB: Execute GROUP BY Query
    DB-->>Model: Returns aggregated rows
    Model-->>Controller: Returns report_data
    deactivate Model
    
    Controller->>View: show_monthly_report_window(report_data)
    View-->>User: Opens New Report Window
    deactivate Controller""",

    "06_export_csv_sequence.png": """sequenceDiagram
    actor User
    participant View as ExpenseView
    participant Controller as ExpenseController
    participant Model as ExpenseModel
    participant OS as File System

    User->>View: Clicks "Export CSV"
    View->>Controller: export_csv()
    
    activate Controller
    Controller->>View: ask_save_file()
    View-->>User: Opens File Save Dialog
    User-->>View: Chooses location (filepath)
    View-->>Controller: Returns filepath
    
    Controller->>Model: get_all_expenses()
    activate Model
    Model-->>Controller: Returns all_expenses
    deactivate Model
    
    Controller->>OS: csv.writer(filepath)
    OS-->>Controller: File saved successfully
    
    Controller->>View: show_success("Data exported")
    deactivate Controller"""
}

# Create a folder for the images
img_dir = "UML_Diagram_Images"
os.makedirs(img_dir, exist_ok=True)

for filename, code in diagrams.items():
    filepath = os.path.join(img_dir, filename)
    generate_image(code, filepath)
