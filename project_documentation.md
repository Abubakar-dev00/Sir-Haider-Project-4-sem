# Expense Tracker Project - Comprehensive Documentation

## 1. Project Overview & Objective
This project is a desktop-based Expense Tracker application built using Python and Tkinter. The primary objective was to practically implement the core concepts of **Software Construction and Development (SDC)**. 

The project strictly adhered to the following academic and industry standards:
- Selection of process models (Iterative / Agile)
- Version control (Git/GitHub)
- Refactoring legacy code
- Software architecture design (Model-View-Controller)
- Unit and Automated testing
- Exception handling
- Code reviews and software process improvement

## 2. Technology Stack
- **Programming Language**: Python 3.x
- **GUI Framework**: Tkinter (Standard Python library) with `ttk` for modern styled widgets
- **Database**: SQLite3 (Local, serverless database)
- **Testing Framework**: `unittest` and `unittest.mock`
- **Version Control**: Git

## 3. Implementation of SDC Concepts

### 3.1. Process Model (Iterative Development)
The project was developed in distinct phases rather than a single waterfall attempt:
- **Phase 1**: Initial setup, Git initialization, and creation of a simulated "Legacy" monolithic codebase.
- **Phase 2**: Refactoring the legacy codebase into a clean architecture (MVC) and applying exception handling.
- **Phase 3**: Implementing automated unit tests to verify system integrity.
- **Phase 4**: Feature expansion (CRUD operations, reporting, data export) and database migration.

### 3.2. Refactoring Legacy Code & Architecture
- **Legacy State**: Initially, the application was a single monolithic script (`legacy_tracker.py`) where UI logic, database queries, and business rules were tightly coupled, simulating poor legacy code.
- **Refactoring Strategy**: The legacy code was completely refactored into the **Model-View-Controller (MVC)** design pattern to achieve separation of concerns:
  - `model.py`: Handles all database connections, schema migrations, and SQL queries.
  - `view.py`: Responsible solely for rendering the Tkinter GUI and capturing user input.
  - `controller.py`: Acts as the orchestrator. It receives user inputs from the View, validates the data, triggers the Model to save it, and then instructs the View to update the display.
  - `main.py`: The entry point that injects the dependencies.

### 3.3. Exception Handling
Robust exception handling was implemented at every layer to prevent application crashes:
- **Database Layer**: All SQL operations (`INSERT`, `UPDATE`, `DELETE`, `SELECT`) are wrapped in `try-except` blocks catching `sqlite3.Error`. If the database file is locked or a query fails, a safe exception is raised rather than terminating the program.
- **Controller/Validation Layer**: User inputs are strictly validated. For instance, if a user attempts to input text into the 'Amount' field, a `ValueError` is caught and a clean error message box is displayed to the user via the UI. Negative amounts and empty fields are also intercepted.

### 3.4. Unit Testing and Automated Testing
- Using Python's built-in `unittest` library, test suites were created for both the Model and Controller.
- `test_model.py`: Tests CRUD operations against an isolated, temporary test database to ensure the real database isn't corrupted during testing.
- `test_controller.py`: Utilizes `unittest.mock.MagicMock` to create dummy View and Model objects. This isolates the Controller's logic, proving that it correctly handles validation errors (like negative numbers) without actually triggering database writes or popping up real GUI windows.

### 3.5. Version Control
- Git was used throughout the project lifecycle.
- Commits were made incrementally to reflect the Agile process (e.g., initial legacy commit, MVC refactoring commit, testing commit, feature expansion commit).
- The code was successfully pushed to a remote GitHub repository, resolving merge conflicts with an existing remote `README`.

## 4. Application Features

The final application is fully functional and includes the following features:
1. **Create Expense**: Users can add an expense with a Date, Category, Description, and Amount.
2. **Read / Display**: Expenses are displayed in a formatted Tkinter Listbox, and a real-time Total is calculated.
3. **Update Expense**: Users can select an existing expense from the list, modify its details in the input fields, and save the changes.
4. **Delete Expense**: Users can permanently remove an expense from the database with a safety confirmation prompt.
5. **Categorization**: Expenses are tagged with categories (`Food`, `Transport`, `Utilities`, `Entertainment`, `Other`).
6. **Monthly Reporting**: A dedicated popup window aggregates all expenses, grouping them by Year-Month and Category to provide actionable financial insights.
7. **CSV Export**: Users can export their entire expense history to a `.csv` file via a file dialog, allowing the data to be opened in Excel or Google Sheets.

## 5. Summary for AI Presentation Generation
*Prompt Instruction for AI Presentation Generator: "Use the sections above to create a 10-slide presentation. Focus heavily on how the software engineering concepts (Iterative process, Refactoring, MVC, Exception Handling, Testing) were applied practically to transform a legacy script into a robust, production-ready desktop application."*
