import pytest
from unittest.mock import Mock, MagicMock
from src.services.bill_service import BillService
from src.models.bill import Bill
from src.validators.bill_validator import ValidationError


class TestBillService:
    """Unit tests for BillService with mocked dependencies."""

    def test_create_bill_success(self):
        """Test successful bill creation with valid data."""
        # Arrange
        mock_repository = Mock()
        mock_validator = Mock()
        mock_calculator = Mock()

        mock_validator.validate.return_value = []
        mock_repository.create.return_value = 123

        service = BillService(mock_repository, mock_validator, mock_calculator)

        # Act
        bill_id = service.create_bill(
            household_id=1,
            payer_id=1,
            title='Electricity Bill',
            amount=150.0,
            category='utilities',
            due_date='2024-12-31'
        )

        # Assert
        assert bill_id == 123
        mock_validator.validate.assert_called_once()
        mock_repository.create.assert_called_once()

    def test_create_bill_validation_fails(self):
        """Test bill creation fails when validation errors occur."""
        # Arrange
        mock_repository = Mock()
        mock_validator = Mock()
        mock_calculator = Mock()

        validation_errors = [
            ValidationError(field='amount', message='Amount must be positive')
        ]
        mock_validator.validate.return_value = validation_errors

        service = BillService(mock_repository, mock_validator, mock_calculator)

        # Act & Assert
        with pytest.raises(ValueError, match="Validation failed"):
            service.create_bill(
                household_id=1,
                payer_id=1,
                title='Invalid Bill',
                amount=-50.0
            )

        mock_validator.validate.assert_called_once()
        mock_repository.create.assert_not_called()

    def test_get_bill(self):
        """Test retrieving a bill by ID."""
        # Arrange
        mock_repository = Mock()
        mock_validator = Mock()
        mock_calculator = Mock()

        expected_bill = Bill(
            bill_id=1,
            household_id=1,
            payer_id=1,
            title='Rent',
            amount=500.0,
            category='rent',
            payment_status='pending'
        )
        mock_repository.find_by_id.return_value = expected_bill

        service = BillService(mock_repository, mock_validator, mock_calculator)

        # Act
        bill = service.get_bill(1)

        # Assert
        assert bill == expected_bill
        mock_repository.find_by_id.assert_called_once_with(1)

    def test_delete_bill(self):
        """Test deleting a bill."""
        # Arrange
        mock_repository = Mock()
        mock_validator = Mock()
        mock_calculator = Mock()

        mock_repository.delete.return_value = True

        service = BillService(mock_repository, mock_validator, mock_calculator)

        # Act
        result = service.delete_bill(1)

        # Assert
        assert result is True
        mock_repository.delete.assert_called_once_with(1)

    def test_update_bill_status_success(self):
        """Test updating bill payment status."""
        # Arrange
        mock_repository = Mock()
        mock_validator = Mock()
        mock_calculator = Mock()

        mock_repository.update.return_value = True

        service = BillService(mock_repository, mock_validator, mock_calculator)

        # Act
        result = service.update_bill_status(1, 'paid')

        # Assert
        assert result is True
        mock_repository.update.assert_called_once_with(1, payment_status='paid')

    def test_update_bill_status_invalid_status(self):
        """Test updating bill with invalid status raises error."""
        # Arrange
        mock_repository = Mock()
        mock_validator = Mock()
        mock_calculator = Mock()

        service = BillService(mock_repository, mock_validator, mock_calculator)

        # Act & Assert
        with pytest.raises(ValueError, match="Status must be one of"):
            service.update_bill_status(1, 'invalid_status')

        mock_repository.update.assert_not_called()

    def test_distribute_bill_success(self):
        """Test bill distribution calculation with strategy."""
        # Arrange
        mock_repository = Mock()
        mock_validator = Mock()
        mock_calculator = Mock()

        test_bill = Bill(
            bill_id=1,
            household_id=1,
            payer_id=1,
            title='Groceries',
            amount=300.0,
            category='food',
            payment_status='pending'
        )
        mock_repository.find_by_id.return_value = test_bill

        expected_distribution = {1: 100.0, 2: 100.0, 3: 100.0}
        mock_calculator.calculate_with_strategy.return_value = expected_distribution

        service = BillService(mock_repository, mock_validator, mock_calculator)
        mock_strategy = Mock()

        # Act
        distribution = service.distribute_bill(
            bill_id=1,
            strategy=mock_strategy,
            participants=[1, 2, 3]
        )

        # Assert
        assert distribution == expected_distribution
        mock_repository.find_by_id.assert_called_once_with(1)
        mock_calculator.calculate_with_strategy.assert_called_once()

    def test_distribute_bill_not_found(self):
        """Test bill distribution fails when bill doesn't exist."""
        # Arrange
        mock_repository = Mock()
        mock_validator = Mock()
        mock_calculator = Mock()

        mock_repository.find_by_id.return_value = None

        service = BillService(mock_repository, mock_validator, mock_calculator)
        mock_strategy = Mock()

        # Act & Assert
        with pytest.raises(ValueError, match="Bill 999 not found"):
            service.distribute_bill(
                bill_id=999,
                strategy=mock_strategy,
                participants=[1, 2, 3]
            )

        mock_calculator.calculate_with_strategy.assert_not_called()