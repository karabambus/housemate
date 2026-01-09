import pytest
from unittest.mock import Mock, patch
from src.facades.housemate_facade import HouseMateFacade


class TestHouseMateFacade:

    @patch('src.facades.housemate_facade.get_db')
    def test_create_bill(self, mock_get_db):
        mock_get_db.return_value = Mock()
        facade = HouseMateFacade()
        facade.bill_service = Mock()
        facade.bill_service.create_bill.return_value = 123

        bill_id = facade.create_bill(
            household_id=1,
            payer_id=5,
            title='Test Bill',
            amount=100.0
        )

        assert bill_id == 123
        facade.bill_service.create_bill.assert_called_once()

    @patch('src.facades.housemate_facade.get_db')
    def test_login(self, mock_get_db):
        mock_get_db.return_value = Mock()
        facade = HouseMateFacade()
        facade.auth_service = Mock()
        mock_user = Mock()
        facade.auth_service.login.return_value = mock_user

        user = facade.login_user('test@example.com', 'password')

        assert user == mock_user
        facade.auth_service.login.assert_called_once_with('test@example.com', 'password')

    @patch('src.facades.housemate_facade.get_db')
    def test_register(self, mock_get_db):
        mock_get_db.return_value = Mock()
        facade = HouseMateFacade()
        facade.auth_service = Mock()
        facade.auth_service.register.return_value = 42

        user_id = facade.register_user('new@test.com', 'pass', 'John', 'Doe')

        assert user_id == 42
        facade.auth_service.register.assert_called_once()
