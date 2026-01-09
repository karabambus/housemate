import pytest
from unittest.mock import Mock
from src.repositories.bill_repository import BillRepository
from src.models.bill import Bill


class TestBillRepository:
    """Unit tests for BillRepository with mocked database."""

    def test_find_by_id_found(self):
        """Test finding a bill by ID when it exists."""
        # Arrange
        mock_db = Mock()
        mock_db.execute_query.return_value = [{
            'bill_id': 1,
            'household_id': 10,
            'payer_id': 5,
            'title': 'Electricity',
            'amount': 150.0,
            'category': 'utilities',
            'is_recurring': 1,
            'frequency': 'monthly',
            'payment_status': 'pending',
            'due_date': '2024-12-31',
            'created_at': '2024-01-01 10:00:00'
        }]

        repository = BillRepository(mock_db)

        # Act
        bill = repository.find_by_id(1)

        # Assert
        assert bill is not None
        assert bill.bill_id == 1
        assert bill.title == 'Electricity'
        assert bill.amount == 150.0
        assert bill.is_recurring is True
        mock_db.execute_query.assert_called_once_with(
            "SELECT * FROM bills WHERE bill_id = ?",
            (1,)
        )

    def test_find_by_id_not_found(self):
        """Test finding a bill by ID when it doesn't exist."""
        # Arrange
        mock_db = Mock()
        mock_db.execute_query.return_value = []

        repository = BillRepository(mock_db)

        # Act
        bill = repository.find_by_id(999)

        # Assert
        assert bill is None
        mock_db.execute_query.assert_called_once()

    def test_find_all(self):
        """Test finding all bills."""
        # Arrange
        mock_db = Mock()
        mock_db.execute_query.return_value = [
            {
                'bill_id': 1,
                'household_id': 10,
                'payer_id': 5,
                'title': 'Rent',
                'amount': 500.0,
                'category': 'rent',
                'is_recurring': 1,
                'frequency': 'monthly',
                'payment_status': 'paid',
                'due_date': '2024-01-01',
                'created_at': '2024-01-01 10:00:00'
            },
            {
                'bill_id': 2,
                'household_id': 10,
                'payer_id': 6,
                'title': 'Groceries',
                'amount': 100.0,
                'category': 'food',
                'is_recurring': 0,
                'frequency': None,
                'payment_status': 'pending',
                'due_date': None,
                'created_at': '2024-01-02 14:00:00'
            }
        ]

        repository = BillRepository(mock_db)

        # Act
        bills = repository.find_all()

        # Assert
        assert len(bills) == 2
        assert bills[0].bill_id == 1
        assert bills[0].title == 'Rent'
        assert bills[1].bill_id == 2
        assert bills[1].title == 'Groceries'
        mock_db.execute_query.assert_called_once()

    def test_find_all_empty(self):
        """Test finding all bills when none exist."""
        # Arrange
        mock_db = Mock()
        mock_db.execute_query.return_value = []

        repository = BillRepository(mock_db)

        # Act
        bills = repository.find_all()

        # Assert
        assert len(bills) == 0
        assert bills == []

    def test_find_by_household(self):
        """Test finding bills by household ID."""
        # Arrange
        mock_db = Mock()
        mock_db.execute_query.return_value = [
            {
                'bill_id': 1,
                'household_id': 10,
                'payer_id': 5,
                'title': 'Water',
                'amount': 50.0,
                'category': 'utilities',
                'is_recurring': 0,
                'frequency': None,
                'payment_status': 'pending',
                'due_date': None,
                'created_at': '2024-01-01 10:00:00'
            }
        ]

        repository = BillRepository(mock_db)

        # Act
        bills = repository.find_by_household(10)

        # Assert
        assert len(bills) == 1
        assert bills[0].household_id == 10
        mock_db.execute_query.assert_called_once_with(
            "SELECT * FROM bills WHERE household_id = ? ORDER BY created_at DESC",
            (10,)
        )

    def test_find_pending_bills(self):
        """Test finding pending bills for a user."""
        # Arrange
        mock_db = Mock()
        mock_db.execute_query.return_value = [
            {
                'bill_id': 3,
                'household_id': 10,
                'payer_id': 5,
                'title': 'Internet',
                'amount': 60.0,
                'category': 'utilities',
                'is_recurring': 1,
                'frequency': 'monthly',
                'payment_status': 'pending',
                'due_date': '2024-02-01',
                'created_at': '2024-01-15 10:00:00'
            }
        ]

        repository = BillRepository(mock_db)

        # Act
        bills = repository.find_pending_bills(5)

        # Assert
        assert len(bills) == 1
        assert bills[0].payment_status == 'pending'
        mock_db.execute_query.assert_called_once()

    def test_create_bill(self):
        """Test creating a new bill."""
        # Arrange
        mock_db = Mock()
        mock_db.execute_insert.return_value = 123  # Simulated bill_id

        repository = BillRepository(mock_db)

        # Act
        bill_id = repository.create(
            household_id=10,
            payer_id=5,
            title='New Bill',
            amount=75.0,
            category='food',
            is_recurring=False,
            frequency=None,
            payment_status='pending',
            due_date='2024-03-01'
        )

        # Assert
        assert bill_id == 123
        mock_db.execute_insert.assert_called_once()
        call_args = mock_db.execute_insert.call_args
        assert 'INSERT INTO bills' in call_args[0][0]

    def test_update_bill(self):
        """Test updating a bill."""
        # Arrange
        mock_db = Mock()
        mock_db.execute_update.return_value = True

        repository = BillRepository(mock_db)

        # Act
        result = repository.update(1, payment_status='paid', amount=200.0)

        # Assert
        assert result is True
        mock_db.execute_update.assert_called_once()
        call_args = mock_db.execute_update.call_args
        assert 'UPDATE bills' in call_args[0][0]
        assert 'WHERE bill_id = ?' in call_args[0][0]

    def test_update_bill_not_found(self):
        """Test updating a bill that doesn't exist."""
        # Arrange
        mock_db = Mock()
        mock_db.execute_update.return_value = False

        repository = BillRepository(mock_db)

        # Act
        result = repository.update(999, payment_status='paid')

        # Assert
        assert result is False
        mock_db.execute_update.assert_called_once()

    def test_delete_bill(self):
        """Test deleting a bill."""
        # Arrange
        mock_db = Mock()
        mock_db.execute_update.return_value = True

        repository = BillRepository(mock_db)

        # Act
        result = repository.delete(1)

        # Assert
        assert result is True
        mock_db.execute_update.assert_called_once_with(
            "DELETE FROM bills WHERE bill_id = ?",
            (1,)
        )

    def test_delete_bill_not_found(self):
        """Test deleting a bill that doesn't exist."""
        # Arrange
        mock_db = Mock()
        mock_db.execute_update.return_value = False

        repository = BillRepository(mock_db)

        # Act
        result = repository.delete(999)

        # Assert
        assert result is False
        mock_db.execute_update.assert_called_once()
