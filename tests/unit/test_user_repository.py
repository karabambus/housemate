import pytest
from unittest.mock import Mock
from src.repositories.user_repository import UserRepository
from src.models.user import User


class TestUserRepository:

    def test_find_by_id_found(self):
        mock_db = Mock()
        mock_db.execute_query.return_value = [{
            'user_id': 1,
            'email': 'test@example.com',
            'password_hash': '$2b$12$hash',
            'first_name': 'John',
            'last_name': 'Doe',
            'created_at': '2024-01-01 10:00:00'
        }]

        repository = UserRepository(mock_db)
        user = repository.find_by_id(1)

        assert user is not None
        assert user.user_id == 1
        assert user.email == 'test@example.com'
        mock_db.execute_query.assert_called_once()

    def test_find_by_id_not_found(self):
        mock_db = Mock()
        mock_db.execute_query.return_value = []

        repository = UserRepository(mock_db)
        user = repository.find_by_id(999)

        assert user is None

    def test_find_by_email_found(self):
        mock_db = Mock()
        mock_db.execute_query.return_value = [{
            'user_id': 5,
            'email': 'alice@test.com',
            'password_hash': '$2b$12$hash',
            'first_name': 'Alice',
            'last_name': 'Wonder',
            'created_at': '2024-01-01 10:00:00'
        }]

        repository = UserRepository(mock_db)
        user = repository.find_by_email('alice@test.com')

        assert user is not None
        assert user.email == 'alice@test.com'
        assert user.first_name == 'Alice'

    def test_find_by_email_not_found(self):
        mock_db = Mock()
        mock_db.execute_query.return_value = []

        repository = UserRepository(mock_db)
        user = repository.find_by_email('nonexistent@test.com')

        assert user is None

    def test_create_user(self):
        mock_db = Mock()
        mock_db.execute_insert.return_value = 42

        repository = UserRepository(mock_db)
        user_id = repository.create_user(
            'newuser@test.com',
            '$2b$12$hashedpassword',
            'New',
            'User'
        )

        assert user_id == 42
        mock_db.execute_insert.assert_called_once()

