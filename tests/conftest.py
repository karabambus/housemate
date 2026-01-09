"""
Pytest configuration and fixtures for testing.

This file provides shared fixtures for both unit and integration tests.
"""
import pytest
import os
import tempfile
from src.infrastructure.database import DatabaseConnection


@pytest.fixture
def test_db():
    """
    Fixture for integration tests - provides a real test database.

    Creates a temporary SQLite database, initializes schema, and cleans up after test.
    """
    # Reset the singleton to allow fresh instance per test
    DatabaseConnection._instance = None
    DatabaseConnection._initialized = False

    # Create temporary database file
    db_fd, db_path = tempfile.mkstemp(suffix='.db')

    # Initialize database connection
    db = DatabaseConnection(db_path)

    # Create tables
    db.execute_update("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    db.execute_update("""
        CREATE TABLE IF NOT EXISTS households (
            household_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    db.execute_update("""
        CREATE TABLE IF NOT EXISTS household_members (
            household_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            joined_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (household_id, user_id),
            FOREIGN KEY (household_id) REFERENCES households(household_id),
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    """)

    db.execute_update("""
        CREATE TABLE IF NOT EXISTS bills (
            bill_id INTEGER PRIMARY KEY AUTOINCREMENT,
            household_id INTEGER NOT NULL,
            payer_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT,
            is_recurring INTEGER DEFAULT 0,
            frequency TEXT,
            payment_status TEXT DEFAULT 'pending',
            due_date DATE,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (household_id) REFERENCES households(household_id),
            FOREIGN KEY (payer_id) REFERENCES users(user_id)
        )
    """)

    db.execute_update("""
        CREATE TABLE IF NOT EXISTS bill_distributions (
            distribution_id INTEGER PRIMARY KEY AUTOINCREMENT,
            bill_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            amount_owed REAL NOT NULL,
            status TEXT DEFAULT 'pending',
            paid_at DATETIME,
            FOREIGN KEY (bill_id) REFERENCES bills(bill_id),
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    """)

    yield db

    # Cleanup: remove temp file (connections auto-close via context manager)
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def sample_users(test_db):
    """
    Fixture that creates sample users in the test database.

    Returns:
        dict: Dictionary with user IDs
    """
    # Create test users
    user1_id = test_db.execute_insert(
        "INSERT INTO users (email, password_hash, first_name, last_name) VALUES (?, ?, ?, ?)",
        ('user1@test.com', '$2b$12$hashedpassword1', 'John', 'Doe')
    )

    user2_id = test_db.execute_insert(
        "INSERT INTO users (email, password_hash, first_name, last_name) VALUES (?, ?, ?, ?)",
        ('user2@test.com', '$2b$12$hashedpassword2', 'Jane', 'Smith')
    )

    user3_id = test_db.execute_insert(
        "INSERT INTO users (email, password_hash, first_name, last_name) VALUES (?, ?, ?, ?)",
        ('user3@test.com', '$2b$12$hashedpassword3', 'Bob', 'Johnson')
    )

    return {
        'user1_id': user1_id,
        'user2_id': user2_id,
        'user3_id': user3_id
    }


@pytest.fixture
def sample_household(test_db, sample_users):
    """
    Fixture that creates a sample household with members.

    Returns:
        int: Household ID
    """
    # Create household
    household_id = test_db.execute_insert(
        "INSERT INTO households (name) VALUES (?)",
        ('Test Household',)
    )

    # Add members to household
    test_db.execute_insert(
        "INSERT INTO household_members (household_id, user_id) VALUES (?, ?)",
        (household_id, sample_users['user1_id'])
    )
    test_db.execute_insert(
        "INSERT INTO household_members (household_id, user_id) VALUES (?, ?)",
        (household_id, sample_users['user2_id'])
    )
    test_db.execute_insert(
        "INSERT INTO household_members (household_id, user_id) VALUES (?, ?)",
        (household_id, sample_users['user3_id'])
    )

    return household_id
