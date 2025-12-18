"""
User Repository

SOLID Principle: Single Responsibility (S)
- This class has ONE responsibility: Database operations for users
- Does NOT handle validation, password hashing, or business logic
"""

from src.models.user import User


class UserRepository:
    """
    Handles database operations for User entities.

    SOLID (S): Only responsible for user data persistence
    """

    def __init__(self, db):
        """
        Initialize repository with database connection.

        Args:
            db: DatabaseConnection instance
        """
        self.db = db

    def find_by_email(self, email):
        """
        Find a user by their email address.

        Args:
            email: User's email address

        Returns:
            User object if found, None otherwise
        """
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

    def find_by_id(self, user_id):
        """
        Find a user by their ID.

        Args:
            user_id: User's ID

        Returns:
            User object if found, None otherwise
        """
        query = "SELECT * FROM users WHERE user_id = ?"
        results = self.db.execute_query(query, (user_id,))

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

    def create_user(self, email, password_hash, first_name, last_name):
        """
        Create a new user in the database.

        Args:
            email: User's email address
            password_hash: Hashed password (bcrypt)
            first_name: User's first name
            last_name: User's last name

        Returns:
            user_id: ID of newly created user
        """
        query = """
            INSERT INTO users (email, password_hash, first_name, last_name)
            VALUES (?, ?, ?, ?)
        """
        user_id = self.db.execute_insert(query, (email, password_hash, first_name, last_name))

        return user_id
