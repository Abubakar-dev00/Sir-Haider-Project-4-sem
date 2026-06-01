# Expense Tracker - Comprehensive UML Diagrams

This document provides professional UML (Unified Modeling Language) diagrams. It includes the overall system architecture and breaks down the system behavior into individual diagrams for **each Functional Requirement (FR)**.

---

## 1. System Architecture (Class Diagram)

The Class Diagram visualizes the static structure of the system, specifically highlighting the **Model-View-Controller (MVC)** design pattern.

```mermaid
classDiagram
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
    ExpenseView --> ExpenseController : Triggers Events
```

---

## 2. Functional Requirements (Sequence Diagrams)

Below are the individual sequence diagrams for each functional requirement, demonstrating the precise data flow and interactions between the MVC components.

### FR-01: Add Expense
Allows the user to input data and save a new expense to the database.

```mermaid
sequenceDiagram
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
    deactivate Controller
```

---

### FR-02: Update Expense
Allows the user to select an existing expense, modify its details, and save the changes.

```mermaid
sequenceDiagram
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
    deactivate Controller
```

---

### FR-03: Delete Expense
Allows the user to select an expense and permanently remove it from the system.

```mermaid
sequenceDiagram
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
    deactivate Controller
```

---

### FR-04: View Monthly Report
Generates and displays an aggregated report of expenses grouped by month and category.

```mermaid
sequenceDiagram
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
    deactivate Controller
```

---

### FR-05: Export to CSV
Allows the user to export all current records to an external CSV file.

```mermaid
sequenceDiagram
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
    deactivate Controller
```
