import pytest
from unittest.mock import Mock, patch, MagicMock
from src.services.auth_service import AuthService
from src.models.user import User


class TestAuthService:
    """Unit tests for AuthService with mocked dependencies."""

    @patch('src.services.auth_service.bcrypt')
    def test_login_success(self, mock_bcrypt):
        """Test successful login with correct credentials."""
        # Arrange
        mock_repository = Mock()
        mock_user = User(
            user_id=1,
            email='test@example.com',
            password_hash='$2b$12$hashedpassword',
            first_name='John',
            last_name='Doe'
        )
        mock_repository.find_by_email.return_value = mock_user
        mock_bcrypt.checkpw.return_value = True

        service = AuthService(mock_repository)

        # Act
        user = service.login('test@example.com', 'correctpassword')

        # Assert
        assert user is not None
        assert user.email == 'test@example.com'
        assert user.user_id == 1
        mock_repository.find_by_email.assert_called_once_with('test@example.com')
        mock_bcrypt.checkpw.assert_called_once()

    @patch('src.services.auth_service.bcrypt')
    def test_login_wrong_password(self, mock_bcrypt):
        """Test login fails with incorrect password."""
        # Arrange
        mock_repository = Mock()
        mock_user = User(
            user_id=1,
            email='test@example.com',
            password_hash='$2b$12$hashedpassword',
            first_name='John',
            last_name='Doe'
        )
        mock_repository.find_by_email.return_value = mock_user
        mock_bcrypt.checkpw.return_value = False  # Wrong password

        service = AuthService(mock_repository)

        # Act
        user = service.login('test@example.com', 'wrongpassword')

        # Assert
        assert user is None
        mock_bcrypt.checkpw.assert_called_once()

    def test_login_user_not_found(self):
        """Test login fails when user doesn't exist."""
        # Arrange
        mock_repository = Mock()
        mock_repository.find_by_email.return_value = None

        service = AuthService(mock_repository)

        # Act
        user = service.login('nonexistent@example.com', 'password')

        # Assert
        assert user is None
        mock_repository.find_by_email.assert_called_once_with('nonexistent@example.com')

    @patch('src.services.auth_service.bcrypt')
    def test_register_success(self, mock_bcrypt):
        """Test successful user registration."""
        # Arrange
        mock_repository = Mock()
        mock_repository.find_by_email.return_value = None  # Email not taken
        mock_repository.create_user.return_value = 42  # New user ID

        mock_bcrypt.gensalt.return_value = b'$2b$12$salt'
        mock_bcrypt.hashpw.return_value = b'$2b$12$hashedpassword'

        service = AuthService(mock_repository)

        # Act
        user_id = service.register(
            email='newuser@example.com',
            password='securepassword',
            first_name='Jane',
            last_name='Smith'
        )

        # Assert
        assert user_id == 42
        mock_repository.find_by_email.assert_called_once_with('newuser@example.com')
        mock_bcrypt.hashpw.assert_called_once()
        mock_repository.create_user.assert_called_once()

        # Verify password was hashed before storing
        call_args = mock_repository.create_user.call_args
        assert call_args[0][0] == 'newuser@example.com'
        assert call_args[0][1] == '$2b$12$hashedpassword'  # Hashed password
        assert call_args[0][2] == 'Jane'
        assert call_args[0][3] == 'Smith'

    def test_register_email_already_exists(self):
        """Test registration fails when email already exists."""
        # Arrange
        mock_repository = Mock()
        existing_user = User(
            user_id=1,
            email='existing@example.com',
            password_hash='$2b$12$hash',
            first_name='Existing',
            last_name='User'
        )
        mock_repository.find_by_email.return_value = existing_user

        service = AuthService(mock_repository)

        # Act & Assert
        with pytest.raises(ValueError, match="Email already registered"):
            service.register(
                email='existing@example.com',
                password='password',
                first_name='New',
                last_name='User'
            )

        mock_repository.find_by_email.assert_called_once_with('existing@example.com')
        mock_repository.create_user.assert_not_called()

    @patch('src.services.auth_service.bcrypt')
    def test_register_password_is_hashed(self, mock_bcrypt):
        """Test that password is properly hashed during registration."""
        # Arrange
        mock_repository = Mock()
        mock_repository.find_by_email.return_value = None
        mock_repository.create_user.return_value = 1

        mock_bcrypt.gensalt.return_value = b'$2b$12$salt'
        mock_bcrypt.hashpw.return_value = b'$2b$12$hashedpassword'

        service = AuthService(mock_repository)

        # Act
        service.register(
            email='test@example.com',
            password='plaintext_password',
            first_name='Test',
            last_name='User'
        )

        # Assert
        # Verify bcrypt.hashpw was called with correct password
        mock_bcrypt.hashpw.assert_called_once()
        call_args = mock_bcrypt.hashpw.call_args
        assert call_args[0][0] == b'plaintext_password'

    @patch('src.services.auth_service.bcrypt')
    def test_login_password_encoding(self, mock_bcrypt):
        """Test that password is correctly encoded for bcrypt."""
        # Arrange
        mock_repository = Mock()
        mock_user = User(
            user_id=1,
            email='test@example.com',
            password_hash='$2b$12$hash',
            first_name='Test',
            last_name='User'
        )
        mock_repository.find_by_email.return_value = mock_user
        mock_bcrypt.checkpw.return_value = True

        service = AuthService(mock_repository)

        # Act
        service.login('test@example.com', 'testpassword')

        # Assert
        # Verify bcrypt.checkpw was called with correctly encoded password
        mock_bcrypt.checkpw.assert_called_once()
        call_args = mock_bcrypt.checkpw.call_args
        assert call_args[0][0] == b'testpassword'  # Password encoded to bytes
        assert call_args[0][1] == b'$2b$12$hash'  # Hash encoded to bytes
