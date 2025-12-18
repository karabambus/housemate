"""
Database infrastructure module.

SOLID Principle: Single Responsibility (S)
- This module has ONE responsibility: managing database connections
- Database schema creation
- Connection pooling
- Query execution utilities
"""

import sqlite3
from pathlib import Path
from contextlib import contextmanager
from typing import Optional, Any, Dict, List
import config


class DatabaseConnection:
    """
    Manages SQLite database connections.

    SOLID Principle: Single Responsibility (S)
    - Only handles database connection management
    - Does NOT handle business logic, validation, or HTTP requests
    """

    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path or str(config.DATABASE_PATH)

    @contextmanager
    def get_connection(self):
        """
        Context manager for database connections.
        Automatically commits on success, rolls back on error.

        Usage:
            with db.get_connection() as conn:
                conn.execute("SELECT * FROM users")
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

    def execute_script(self, script_path: str):
        """
        Execute SQL script file.
        Used for schema creation and seed data loading.
        """
        with open(script_path, 'r') as f:
            sql_script = f.read()

        with self.get_connection() as conn:
            conn.executescript(sql_script)

    def execute_query(self, query: str, params: tuple = ()) -> List[sqlite3.Row]:
        """
        Execute a SELECT query and return results.
        """
        with self.get_connection() as conn:
            cursor = conn.execute(query, params)
            return cursor.fetchall()

    def execute_update(self, query: str, params: tuple = ()) -> int:
        """
        Execute INSERT, UPDATE, or DELETE query.
        Returns the number of affected rows.
        """
        with self.get_connection() as conn:
            cursor = conn.execute(query, params)
            return cursor.rowcount

    def execute_insert(self, query: str, params: tuple = ()) -> int:
        """
        Execute INSERT query and return the last inserted row ID.
        """
        with self.get_connection() as conn:
            cursor = conn.execute(query, params)
            return cursor.lastrowid


def init_db(reset: bool = False):
    """
    Initialize the database with schema and seed data.

    Args:
        reset: If True, deletes existing database and creates fresh one
    """
    db_path = Path(config.DATABASE_PATH)

    # Create database directory if it doesn't exist
    db_path.parent.mkdir(parents=True, exist_ok=True)

    # Remove existing database if reset requested
    if reset and db_path.exists():
        db_path.unlink()
        print(f"Removed existing database: {db_path}")

    # Create database connection
    db = DatabaseConnection(str(db_path))

    # Load schema
    schema_path = db_path.parent / 'schema.sql'
    if schema_path.exists():
        print(f"Loading schema from: {schema_path}")
        db.execute_script(str(schema_path))
        print("✓ Database schema created successfully")
    else:
        print(f"Warning: Schema file not found at {schema_path}")

    # Load seed data
    seed_path = db_path.parent / 'seed_data.sql'
    if seed_path.exists():
        print(f"Loading seed data from: {seed_path}")
        db.execute_script(str(seed_path))
        print("✓ Seed data loaded successfully")
    else:
        print(f"Warning: Seed data file not found at {seed_path}")

    print(f"\n✓ Database initialized at: {db_path}")


def get_db() -> DatabaseConnection:
    """
    Factory function to get database connection instance.

    SOLID Principle: Dependency Inversion (D)
    - Repositories will depend on this abstraction
    - Not on concrete SQLite implementation
    """
    return DatabaseConnection()


if __name__ == '__main__':
    # Initialize database when run directly
    print("Initializing HouseMate database...")
    init_db(reset=True)

    # Test connection
    db = get_db()
    users = db.execute_query("SELECT COUNT(*) as count FROM users")
    print(f"\nTest query: {users[0]['count']} users in database")
