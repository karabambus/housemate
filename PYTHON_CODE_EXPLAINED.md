# Python Code Explained - HouseMate Project

This document explains all the Python code we've written so far, focusing on Python-specific concepts and SOLID principles.

---

## Table of Contents

1. [Project Structure](#project-structure)
2. [Python Packages and Modules](#python-packages-and-modules)
3. [Configuration (config.py)](#configuration-configpy)
4. [Database Infrastructure](#database-infrastructure)
5. [Flask Application (app.py)](#flask-application-apppy)
6. [Understanding SOLID in Our Code](#understanding-solid-in-our-code)
7. [What You Need for Authentication](#what-you-need-for-authentication)

---

## Project Structure

```
housemate/
├── app.py                      # Main Flask application
├── config.py                   # Configuration settings
├── requirements.txt            # Python dependencies
├── database/
│   ├── schema.sql             # Database schema (SQL)
│   ├── seed_data.sql          # Test data (SQL)
│   └── housemate.db           # SQLite database file
├── src/                       # Python source code
│   ├── __init__.py            # Makes 'src' a package
│   ├── models/                # Data models (User, Bill, etc.)
│   │   └── __init__.py
│   ├── interfaces/            # Abstract interfaces (SOLID I, D)
│   │   └── __init__.py
│   ├── repositories/          # Database access (SOLID S)
│   │   └── __init__.py
│   ├── services/              # Business logic (SOLID D)
│   │   └── __init__.py
│   ├── strategies/            # Strategy pattern (SOLID O, L)
│   │   └── __init__.py
│   ├── validators/            # Validation logic (SOLID S)
│   │   └── __init__.py
│   ├── infrastructure/        # Technical infrastructure
│   │   ├── __init__.py
│   │   └── database.py        # Database connection helper
│   └── controllers/           # HTTP request handlers (SOLID S)
│       └── __init__.py
├── templates/                 # HTML templates (Jinja2)
└── static/                    # CSS, JavaScript, images
```

---

## Python Packages and Modules

### What is `__init__.py`?

Every directory with `__init__.py` becomes a **Python package** that can be imported.

```python
# Without __init__.py
from database import get_db  # ❌ ERROR: 'database' is not a package

# With __init__.py in src/infrastructure/
from src.infrastructure.database import get_db  # ✅ WORKS
```

**Our `__init__.py` files are empty** - they just mark directories as packages.

### Import Styles in Python

```python
# Style 1: Import module
import config
print(config.DATABASE_PATH)

# Style 2: Import specific items
from config import DATABASE_PATH
print(DATABASE_PATH)

# Style 3: Import with alias
from src.infrastructure import database as db
conn = db.get_db()

# Style 4: Import everything (NOT RECOMMENDED)
from config import *
```

---

## Configuration (config.py)

### What Does This File Do?

Stores all application settings in ONE place (SOLID: Single Responsibility).

```python
"""
Configuration settings for HouseMate application.
"""
import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent
```

**Explanation:**
- `__file__` = path to current file (config.py)
- `Path(__file__).parent` = parent directory of config.py (the `housemate/` folder)

```python
# Database
DATABASE_PATH = BASE_DIR / 'database' / 'housemate.db'
```

**Explanation:**
- `Path` objects can be combined with `/` operator
- `BASE_DIR / 'database' / 'housemate.db'` creates path: `housemate/database/housemate.db`
- **Much better than string concatenation!**

```python
# Flask
SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
DEBUG = os.environ.get('DEBUG', 'True') == 'True'
```

**Explanation:**
- `os.environ.get('KEY', 'default')` reads environment variable or uses default
- Used for security: different keys in development vs production
- `DEBUG = True` enables Flask debug mode (auto-reload, detailed errors)

```python
# Upload settings
UPLOAD_FOLDER = BASE_DIR / 'static' / 'uploads'
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}
```

**Explanation:**
- `16 * 1024 * 1024` = 16 megabytes in bytes
- `{'png', 'jpg'}` is a **set** (unordered, unique items)
- Used to validate file uploads (receipt images)

---

## Database Infrastructure

### File: `src/infrastructure/database.py`

This is the **most important Python file** to understand!

#### Class: `DatabaseConnection`

```python
class DatabaseConnection:
    """
    Manages SQLite database connections.

    SOLID Principle: Single Responsibility (S)
    - Only handles database connection management
    - Does NOT handle business logic, validation, or HTTP requests
    """

    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path or str(config.DATABASE_PATH)
```

**Python Concepts:**

1. **Type Hints**: `db_path: Optional[str] = None`
   - `Optional[str]` means "string or None"
   - Type hints are **optional** in Python but help with documentation
   - IDEs use them for autocomplete

2. **Default Parameters**: `= None`
   - If no argument provided, `db_path` defaults to `None`

3. **`or` operator trick**: `db_path or str(config.DATABASE_PATH)`
   - If `db_path` is `None`, use `config.DATABASE_PATH`
   - Short way to write: `if db_path is None: db_path = config.DATABASE_PATH`

4. **`self.db_path`**: Instance variable
   - Stores the database path for this specific instance
   - Can be accessed anywhere in the class with `self.db_path`

#### Context Manager: `get_connection()`

```python
@contextmanager
def get_connection(self):
    """
    Context manager for database connections.
    Automatically commits on success, rolls back on error.
    """
    conn = sqlite3.connect(self.db_path)
    conn.row_factory = sqlite3.Row  # Access columns by name
    conn.execute("PRAGMA foreign_keys = ON")  # Enable foreign key constraints
    try:
        yield conn
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()
```

**Python Concepts:**

1. **Decorator**: `@contextmanager`
   - From `contextlib` module
   - Makes this function work with `with` statement
   - Decorator = function that modifies another function

2. **Context Manager Pattern**:
   ```python
   with db.get_connection() as conn:
       conn.execute("SELECT * FROM users")
   # Connection automatically closed here!
   ```

3. **`yield` keyword**:
   - Like `return` but function can resume after
   - Everything before `yield` runs when entering `with` block
   - Everything after `yield` runs when exiting `with` block

4. **Try-Except-Finally**:
   ```python
   try:
       # Try this code
       yield conn
       conn.commit()  # Save changes if no error
   except Exception as e:
       # If error occurs
       conn.rollback()  # Undo changes
       raise e         # Re-raise the error
   finally:
       # Always runs (error or not)
       conn.close()    # Close connection
   ```

5. **`sqlite3.Row`**:
   - Makes results accessible by column name
   - Example:
     ```python
     cursor = conn.execute("SELECT email, first_name FROM users")
     row = cursor.fetchone()

     # Without Row factory:
     email = row[0]  # Position-based

     # With Row factory:
     email = row['email']  # Name-based (better!)
     ```

#### Method: `execute_script()`

```python
def execute_script(self, script_path: str):
    """
    Execute SQL script file.
    Used for schema creation and seed data loading.
    """
    with open(script_path, 'r') as f:
        sql_script = f.read()

    with self.get_connection() as conn:
        conn.executescript(sql_script)
```

**Python Concepts:**

1. **File Reading**:
   ```python
   with open(script_path, 'r') as f:
       sql_script = f.read()
   ```
   - `'r'` = read mode
   - `f.read()` reads entire file as string
   - `with` automatically closes file

2. **Nested Context Managers**:
   ```python
   with open(...) as f:
       # File is open
       with self.get_connection() as conn:
           # Database is connected
           conn.executescript(...)
       # Database closed
   # File closed
   ```

#### Method: `execute_query()`

```python
def execute_query(self, query: str, params: tuple = ()) -> List[sqlite3.Row]:
    """
    Execute a SELECT query and return results.
    """
    with self.get_connection() as conn:
        cursor = conn.execute(query, params)
        return cursor.fetchall()
```

**Python Concepts:**

1. **Return Type Hint**: `-> List[sqlite3.Row]`
   - Function returns a list of Row objects

2. **Parameters**:
   ```python
   # BAD - SQL Injection vulnerability:
   query = f"SELECT * FROM users WHERE email = '{email}'"

   # GOOD - Parameterized query:
   query = "SELECT * FROM users WHERE email = ?"
   params = (email,)  # Tuple with one item
   cursor = conn.execute(query, params)
   ```

3. **Empty tuple default**: `params: tuple = ()`
   - If no parameters, use empty tuple
   - Allows calling: `execute_query("SELECT * FROM users")`

#### Function: `init_db()`

```python
def init_db(reset: bool = False):
    """
    Initialize the database with schema and seed data.
    """
    db_path = Path(config.DATABASE_PATH)

    # Create database directory if it doesn't exist
    db_path.parent.mkdir(parents=True, exist_ok=True)
```

**Python Concepts:**

1. **Path.mkdir()**:
   - `parents=True` - create parent directories if they don't exist
   - `exist_ok=True` - don't error if directory already exists

2. **Conditional deletion**:
   ```python
   if reset and db_path.exists():
       db_path.unlink()  # Delete file
   ```

3. **Path.exists()**: Check if file exists
4. **Path.unlink()**: Delete file

#### Function: `get_db()`

```python
def get_db() -> DatabaseConnection:
    """
    Factory function to get database connection instance.

    SOLID Principle: Dependency Inversion (D)
    - Repositories will depend on this abstraction
    - Not on concrete SQLite implementation
    """
    return DatabaseConnection()
```

**Python Concepts:**

1. **Factory Pattern**:
   - Function that creates and returns objects
   - Hides implementation details
   - Easy to swap implementations later:
     ```python
     # Now: SQLite
     return DatabaseConnection()

     # Future: PostgreSQL
     return PostgresConnection()
     ```

2. **Return type**: `-> DatabaseConnection`
   - Documents what type is returned

---

## Flask Application (app.py)

### Flask Basics

```python
from flask import Flask, render_template, session, redirect, url_for, flash, request

# Create Flask application
app = Flask(__name__)
app.config.from_object(config)
```

**Explanation:**

1. **`Flask(__name__)`**:
   - Creates Flask application instance
   - `__name__` = name of current module (usually `"app"`)
   - Flask uses this to find templates/static files

2. **`app.config.from_object(config)`**:
   - Loads all UPPERCASE variables from `config.py`
   - `config.SECRET_KEY` → `app.config['SECRET_KEY']`
   - `config.DEBUG` → `app.config['DEBUG']`

### Routes (URL Mapping)

```python
@app.route('/')
def index():
    """Landing page / dashboard."""
    if 'user_id' in session:
        return render_template('dashboard.html',
                             user_name=session.get('user_name'),
                             household_name=session.get('household_name'))
    else:
        return render_template('index.html')
```

**Python Concepts:**

1. **Decorator**: `@app.route('/')`
   - Maps URL `/` to function `index()`
   - When user visits `http://localhost:5000/`, Flask calls `index()`

2. **Session (Dictionary-like)**:
   ```python
   # Check if key exists
   if 'user_id' in session:

   # Get value (returns None if not found)
   user_name = session.get('user_name')

   # Set value
   session['user_id'] = 123
   ```

3. **`render_template()`**:
   - Loads HTML template from `templates/` folder
   - Passes variables to template:
     ```python
     render_template('dashboard.html',
                    user_name="Marin",      # {{ user_name }} in template
                    household_name="Home")  # {{ household_name }} in template
     ```

### Error Handlers

```python
@app.errorhandler(404)
def page_not_found(e):
    """404 error handler."""
    return render_template('404.html'), 404
```

**Explanation:**
- `@app.errorhandler(404)` catches 404 errors
- `return template, status_code` - tuple return
- Flask sends status code 404 to browser

### Context Processor

```python
@app.context_processor
def inject_config():
    """Inject configuration variables into all templates."""
    return {
        'app_name': config.APP_NAME,
        'version': config.VERSION,
    }
```

**Explanation:**
- Makes variables available in **ALL** templates
- No need to pass `app_name` to every `render_template()` call
- Template can use: `{{ app_name }}`, `{{ version }}`

### Running the App

```python
if __name__ == '__main__':
    # This runs only when executing: python app.py
    # NOT when importing: from app import app

    from src.infrastructure.database import init_db
    db_path = Path(config.DATABASE_PATH)
    if not db_path.exists():
        init_db()

    app.run(debug=config.DEBUG, host='0.0.0.0', port=5000)
```

**Python Concepts:**

1. **`if __name__ == '__main__':`**:
   - `__name__` is special variable
   - When running file directly: `__name__ == '__main__'`
   - When importing file: `__name__ == 'app'`
   - Prevents code from running when imported

2. **`app.run()` parameters**:
   - `debug=True` - auto-reload on code changes, detailed errors
   - `host='0.0.0.0'` - accessible from network (not just localhost)
   - `port=5000` - run on port 5000

---

## Understanding SOLID in Our Code

### Single Responsibility (S)

**Example: `DatabaseConnection` class**

```python
class DatabaseConnection:
    # ✅ ONE responsibility: Manage database connections
    def get_connection(self): ...
    def execute_query(self, query, params): ...
    def execute_update(self, query, params): ...
```

**NOT like this:**

```python
class DatabaseConnection:
    # ❌ MULTIPLE responsibilities (violates SRP)
    def get_connection(self): ...
    def validate_user(self, user): ...        # Should be in Validator
    def send_email(self, to, message): ...    # Should be in EmailService
    def generate_pdf(self, data): ...         # Should be in PDFGenerator
```

**Why is this good?**
- If we change database from SQLite to PostgreSQL, we only change `DatabaseConnection`
- If we change email service, `DatabaseConnection` is not affected
- Each class has **one reason to change**

---

## What You Need for Authentication

Now that you understand the Python code, here's what you'll implement:

### 1. User Model (`src/models/user.py`)

**Purpose**: Represent a user (data only, no logic)

```python
class User:
    """SOLID (S): Only represents user data"""

    def __init__(self, user_id, email, password_hash, first_name, last_name):
        self.user_id = user_id
        self.email = email
        self.password_hash = password_hash
        self.first_name = first_name
        self.last_name = last_name

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
```

**Key Python Concepts**:
- `__init__`: Constructor (runs when creating: `user = User(...)`)
- `self`: Reference to the instance
- `f"{var}"`: f-string (formatted string)

### 2. User Repository (`src/repositories/user_repository.py`)

**Purpose**: Database operations for users (SOLID S - Single Responsibility)

```python
class UserRepository:
    """SOLID (S): Only handles database operations"""

    def __init__(self, db):
        self.db = db  # DatabaseConnection instance

    def find_by_email(self, email):
        """Find user by email"""
        query = "SELECT * FROM users WHERE email = ?"
        results = self.db.execute_query(query, (email,))

        if results:
            row = results[0]
            return User(
                user_id=row['user_id'],
                email=row['email'],
                password_hash=row['password_hash'],
                first_name=row['first_name'],
                last_name=row['last_name']
            )
        return None

    def create(self, email, password_hash, first_name, last_name):
        """Create new user"""
        query = """
            INSERT INTO users (email, password_hash, first_name, last_name)
            VALUES (?, ?, ?, ?)
        """
        user_id = self.db.execute_insert(query,
                                         (email, password_hash, first_name, last_name))
        return user_id
```

**Key Python Concepts**:
- Tuple with one item: `(email,)` - note the comma!
- Multi-line string: `""" ... """`
- Returning `None` means "not found"

### 3. Auth Service (`src/services/auth_service.py`)

**Purpose**: Business logic for login/register

```python
import bcrypt

class AuthService:
    """SOLID (S): Only handles authentication logic"""

    def __init__(self, user_repository):
        self.user_repository = user_repository

    def login(self, email, password):
        """Login user - returns User or None"""
        user = self.user_repository.find_by_email(email)

        if user and bcrypt.checkpw(password.encode('utf-8'),
                                   user.password_hash.encode('utf-8')):
            return user
        return None

    def register(self, email, password, first_name, last_name):
        """Register new user"""
        # Check if email exists
        existing = self.user_repository.find_by_email(email)
        if existing:
            return None  # Email already exists

        # Hash password
        password_hash = bcrypt.hashpw(password.encode('utf-8'),
                                     bcrypt.gensalt())

        # Create user
        user_id = self.user_repository.create(email,
                                             password_hash.decode('utf-8'),
                                             first_name,
                                             last_name)
        return user_id
```

**Key Python Concepts**:
- `password.encode('utf-8')`: Convert string to bytes
- `password_hash.decode('utf-8')`: Convert bytes to string
- `bcrypt.checkpw()`: Compare password with hash (returns True/False)

### 4. Flask Routes (in `app.py`)

```python
from flask import request, session, redirect, url_for, flash
from src.services.auth_service import AuthService
from src.repositories.user_repository import UserRepository
from src.infrastructure.database import get_db

# Create instances (Dependency Injection)
db = get_db()
user_repo = UserRepository(db)
auth_service = AuthService(user_repo)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get form data
        email = request.form.get('email')
        password = request.form.get('password')

        # Try to login
        user = auth_service.login(email, password)

        if user:
            # Login successful - set session
            session['user_id'] = user.user_id
            session['user_name'] = user.get_full_name()
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            # Login failed
            flash('Invalid email or password', 'danger')

    return render_template('auth/login.html')

@app.route('/logout')
def logout():
    session.clear()  # Remove all session data
    flash('Logged out successfully', 'info')
    return redirect(url_for('index'))
```

**Key Python Concepts**:
- `request.method`: 'GET' or 'POST'
- `request.form.get('email')`: Get form field value
- `flash('message', 'category')`: Show message to user (appears once)
- `redirect(url_for('index'))`: Redirect to `index()` function
- `url_for('index')`: Generate URL for function (don't hardcode URLs!)

---

## Summary: What You'll Code

1. **User Model** - Simple class with data
2. **UserRepository** - Database queries (SELECT, INSERT)
3. **AuthService** - Login/register logic with bcrypt
4. **Flask Routes** - Handle form submissions
5. **HTML Templates** - Login and register forms

**Python Skills You'll Practice**:
- Classes and `__init__`
- Working with `self`
- Database queries with parameters
- Password hashing with bcrypt
- Flask request handling
- Session management
- Form data processing

---

## Quick Reference

### Common Python Patterns

```python
# Check if variable is None
if user is None:
if not user:  # Shorter way

# Ternary operator
result = value1 if condition else value2

# Dictionary get with default
email = user.get('email', 'unknown@example.com')

# List comprehension
emails = [user['email'] for user in users]

# String formatting
name = f"{first} {last}"  # f-string (modern)
name = "{} {}".format(first, last)  # format() (older)

# Multiple return values
def get_user():
    return user, error  # Returns tuple
user, error = get_user()  # Unpack tuple
```

### Debugging Tips

```python
# Print variables
print(f"User: {user}")
print(f"Type: {type(user)}")

# Check if object has attribute
if hasattr(user, 'email'):
    print(user.email)

# See all attributes
print(dir(user))

# Python debugger (pdb)
import pdb; pdb.set_trace()  # Pause here
```

---

Now you're ready to code authentication! Ask me if anything is unclear! 🚀
