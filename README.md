# LibriCore - Professional Library Management System

A full-stack, enterprise-grade Library Management System built with **Flask**, **SQLAlchemy**, **Flask-Login**, **Flask-WTF**, and **Bootstrap 5**.

---

## 🌟 Key Features

1. **Role-Based Authentication**:
   - Secure registration, login, session management, and logout.
   - Separate permissions for **Admin** and **Student**.
   - URL-level authorization decorators (`@admin_required`).
   - Werkzeug secure password hashing (PBKDF2/SHA256).

2. **Book & Inventory Management**:
   - Search books by Title, Author, ISBN, or Category.
   - Category filtering & availability status filters (In Stock / Out of Stock).
   - Pagination support for fast loading.
   - Admin CRUD (Create, Read, Update, Delete) with protection against deleting books currently on loan.

3. **Issue & Return Workflow**:
   - Automatic due date generation (configurable borrowing window, default 14 days).
   - Atomic inventory decrement on issue, and increment on return.
   - Max borrow limits per student (default 3 books).
   - Out-of-stock and duplicate loan prevention.
   - Protection against returning another student's loan.

4. **Automated Late Fine Calculation**:
   - Configurable daily fine rate (default ₹5.00/day).
   - Automatic overdue calculation: `(return_date - due_date) * rate`.
   - Dynamic fine tracking for active overdue books.
   - Fine payment recording mechanism.

5. **Dashboards**:
   - **Student Dashboard**: Live stats of books issued, books returned, overdue items, pending fines, and quick-return buttons.
   - **Admin Dashboard**: System-wide analytics, total users, copies available, overdue alerts, most-borrowed books chart, and rules management.

---

## 🚀 Quick Start Guide (Windows)

### 1. Open Terminal in VS Code
Open the project folder (`d:/library system`) in VS Code, then open PowerShell (`Ctrl + \``).

### 2. Activate Virtual Environment
```powershell
.\venv\Scripts\Activate.ps1
```
*(If script execution is disabled on Windows, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` first).*

### 3. Initialize & Seed Database
```powershell
python seed.py
```
This automatically initializes the SQLite database schema and populates sample books, an admin account, and a test student account.

### 4. Run the Application
```powershell
python run.py
```
Open your browser and visit: **`http://127.0.0.1:5000`**

---

## 🔑 Default Credentials

| Role | Email | Password |
|---|---|---|
| **Admin** | `admin@library.com` | `Admin@12345` |
| **Student** | `student@library.com` | `Student@12345` |

*(You can also register a brand new student account from the Register page).*

---

## 🧪 Running Automated Unit Tests
To verify all business rules, stock controls, and authorization checks:
```powershell
python -m unittest discover -s tests -v
```

---

## 📂 Project Structure
```text
d:/library system/
│── app/
│   │── __init__.py         # Application Factory (create_app), extensions
│   │── config.py           # Multi-environment configs (Dev, Test, Prod)
│   │── models.py           # User, Book, Loan, LibrarySettings models
│   │── forms.py            # Flask-WTF validation forms
│   │── decorators.py       # @admin_required access guard
│   │── routes/
│   │   │── auth.py         # Login, Register, Logout
│   │   │── main.py         # Catalog, Search, Book Details
│   │   │── student.py      # Student Dashboard, Issue, Return, History
│   │   │── admin.py        # Admin Overview, Book CRUD, Loans, Rules
│   │── static/             # Custom CSS and JavaScript
│   │── templates/          # Jinja2 HTML templates
│── tests/
│   │── test_library.py     # 9 comprehensive unit tests
│── .env                    # Environment secrets
│── requirements.txt        # Dependencies
│── seed.py                 # Initial database seeding script
│── run.py                  # Server entry point
```
