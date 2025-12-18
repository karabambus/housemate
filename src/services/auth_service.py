"""
Authentication Service

SOLID Principle: Single Responsibility (S)
- This class has ONE responsibility: User authentication logic
- Does NOT handle HTTP requests, database queries, or validation
"""

import bcrypt


class AuthService:
    """
    Handles user authentication (login, register).

    SOLID (S): Only responsible for authentication business logic
    SOLID (D): Depends on UserRepository abstraction, not concrete implementation
    """

    def __init__(self, user_repository):
        """
        Initialize service with user repository.

        Args:
            user_repository: UserRepository instance (Dependency Injection)
        """
        self.user_repository = user_repository

    def login(self, email, password):
        """
        Authenticate user with email and password.

        Args:
            email: User's email
            password: Plain text password

        Returns:
            User object if authentication successful, None otherwise
        """
        user = self.user_repository.find_by_email(email)

        # bcrypt.checkpw() compares plain password with stored hash
        # It extracts the salt from the hash and re-hashes the password with it
        # DO NOT hash the password yourself before calling checkpw()!
        if user and bcrypt.checkpw(password.encode('utf-8'),
                                   user.password_hash.encode('utf-8')):
            return user
        return None

    def register(self, email, password, first_name, last_name):
        """
        Register a new user.

        Args:
            email: User's email
            password: Plain text password (will be hashed)
            first_name: User's first name
            last_name: User's last name

        Returns:
            user_id: ID of newly created user

        Raises:
            ValueError: If email already registered
        """
        # Check if email already exists
        existing_user = self.user_repository.find_by_email(email)
        if existing_user:
            raise ValueError("Email already registered")

        # Hash password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Create new user (convert bytes to string for database)
        user_id = self.user_repository.create_user(
            email,
            hashed_password.decode('utf-8'),  # Convert bytes to string
            first_name,
            last_name
        )

        return user_id
