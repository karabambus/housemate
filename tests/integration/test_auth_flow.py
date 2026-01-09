"""
Integration tests for Authentication flow.

These tests use a real database (no mocks) and test the full stack:
- Repository -> Service -> Business Logic
- Real bcrypt hashing
- Database interactions

IMPORTANT: These are integration tests without mocks (I8 - 1 bod requirement)
"""
import pytest
from src.repositories.user_repository import UserRepository
from src.services.auth_service import AuthService


@pytest.mark.integration
class TestAuthFlowIntegration:
    """Integration tests for complete authentication flow without mocks."""

    def test_register_and_login(self, test_db):
        """Test full registration and login flow."""
        # Arrange
        repository = UserRepository(test_db)
        service = AuthService(repository)

        # Act - Register new user
        user_id = service.register(
            email='newuser@test.com',
            password='securepassword123',
            first_name='Alice',
            last_name='Wonder'
        )

        # Act - Login with correct credentials
        user = service.login('newuser@test.com', 'securepassword123')

        # Assert
        assert user_id is not None
        assert user is not None
        assert user.user_id == user_id
        assert user.email == 'newuser@test.com'
        assert user.first_name == 'Alice'
        assert user.last_name == 'Wonder'

    def test_login_with_wrong_password(self, test_db):
        """Test that login fails with incorrect password."""
        # Arrange
        repository = UserRepository(test_db)
        service = AuthService(repository)

        # Register user
        service.register(
            email='testuser@test.com',
            password='correctpassword',
            first_name='Test',
            last_name='User'
        )

        # Act - Try to login with wrong password
        user = service.login('testuser@test.com', 'wrongpassword')

        # Assert
        assert user is None

    def test_register_duplicate_email(self, test_db):
        """Test that registration fails with duplicate email."""
        # Arrange
        repository = UserRepository(test_db)
        service = AuthService(repository)

        # Register first user
        service.register(
            email='duplicate@test.com',
            password='password1',
            first_name='First',
            last_name='User'
        )

        # Act & Assert - Try to register with same email
        with pytest.raises(ValueError, match="Email already registered"):
            service.register(
                email='duplicate@test.com',
                password='password2',
                first_name='Second',
                last_name='User'
            )

    def test_login_nonexistent_user(self, test_db):
        """Test that login fails for non-existent user."""
        # Arrange
        repository = UserRepository(test_db)
        service = AuthService(repository)

        # Act - Try to login with non-existent email
        user = service.login('nonexistent@test.com', 'anypassword')

        # Assert
        assert user is None

    def test_password_is_hashed_in_database(self, test_db):
        """Test that passwords are stored as hashes, not plaintext."""
        # Arrange
        repository = UserRepository(test_db)
        service = AuthService(repository)
        plain_password = 'mysecretpassword'

        # Act - Register user
        user_id = service.register(
            email='secure@test.com',
            password=plain_password,
            first_name='Secure',
            last_name='User'
        )

        # Act - Retrieve user directly from repository
        user = repository.find_by_id(user_id)

        # Assert - Password should be hashed (starts with $2b$ for bcrypt)
        assert user is not None
        assert user.password_hash != plain_password
        assert user.password_hash.startswith('$2b$')

    def test_multiple_users_registration(self, test_db):
        """Test registering multiple users."""
        # Arrange
        repository = UserRepository(test_db)
        service = AuthService(repository)

        # Act - Register multiple users
        user1_id = service.register(
            'user1@test.com', 'password1', 'User', 'One'
        )
        user2_id = service.register(
            'user2@test.com', 'password2', 'User', 'Two'
        )
        user3_id = service.register(
            'user3@test.com', 'password3', 'User', 'Three'
        )

        # Assert - All users can login
        assert service.login('user1@test.com', 'password1') is not None
        assert service.login('user2@test.com', 'password2') is not None
        assert service.login('user3@test.com', 'password3') is not None

        # Assert - User IDs are unique
        assert user1_id != user2_id
        assert user2_id != user3_id
        assert user1_id != user3_id

    def test_case_sensitive_email(self, test_db):
        """Test that email matching is case-sensitive."""
        # Arrange
        repository = UserRepository(test_db)
        service = AuthService(repository)

        # Register with lowercase email
        service.register(
            'testcase@test.com',
            'password',
            'Test',
            'Case'
        )

        # Act - Try to login with different case
        user_lower = service.login('testcase@test.com', 'password')
        user_upper = service.login('TESTCASE@TEST.COM', 'password')

        # Assert - Exact match works, case mismatch fails
        assert user_lower is not None
        assert user_upper is None

    def test_user_repository_find_by_email(self, test_db):
        """Test finding user by email through repository."""
        # Arrange
        repository = UserRepository(test_db)
        service = AuthService(repository)

        # Register user
        service.register(
            'findme@test.com',
            'password',
            'Find',
            'Me'
        )

        # Act - Find user by email
        user = repository.find_by_email('findme@test.com')

        # Assert
        assert user is not None
        assert user.email == 'findme@test.com'
        assert user.first_name == 'Find'
        assert user.last_name == 'Me'
