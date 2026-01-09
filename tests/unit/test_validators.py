from src.validators.bill_validator import BillValidator


class TestBillValidator:
    """Unit tests for BillValidator."""

    def test_valid_bill_passes_validation(self):
        """Test that valid bill data passes validation."""
        # Arrange
        validator = BillValidator()
        bill_data = {
            'household_id': 1,
            'payer_id': 1,
            'title': 'Electricity Bill',
            'amount': 120.50,
            'category': 'utilities',
            'due_date': '2024-12-01'
        }

        # Act
        errors = validator.validate(bill_data)

        # Assert
        assert len(errors) == 0

    def test_missing_title_fails_validation(self):
        """Test that missing title fails validation."""
        # Arrange
        validator = BillValidator()
        bill_data = {
            'household_id': 1,
            'payer_id': 1,
            'amount': 75.00,
            'due_date': '2024-11-15'
        }

        # Act
        errors = validator.validate(bill_data)

        # Assert
        assert len(errors) > 0
        assert any(error.field == 'title' for error in errors)

    def test_negative_amount_fails_validation(self):
        """Test that negative amount fails validation."""
        # Arrange
        validator = BillValidator()
        bill_data = {
            'household_id': 1,
            'payer_id': 1,
            'title': 'Water Bill',
            'amount': -50.00,
            'due_date': '2024-10-10'
        }

        # Act
        errors = validator.validate(bill_data)

        # Assert
        assert len(errors) > 0
        assert any(error.field == 'amount' for error in errors)

    def test_invalid_category_fails_validation(self):
        """Test that invalid category fails validation."""
        # Arrange
        validator = BillValidator()
        bill_data = {
            'household_id': 1,
            'payer_id': 1,
            'title': 'Internet Bill',
            'amount': 60.00,
            'due_date': '2024-09-20',
            'category': 'invalid_category'
        }

        # Act
        errors = validator.validate(bill_data)

        # Assert
        assert len(errors) > 0
        assert any(error.field == 'category' for error in errors)

    def test_missing_household_id_fails_validation(self):
        """Test that missing household_id fails validation."""
        # Arrange
        validator = BillValidator()
        bill_data = {
            'payer_id': 1,
            'title': 'Rent',
            'amount': 500.00
        }

        # Act
        errors = validator.validate(bill_data)

        # Assert
        assert len(errors) > 0
        assert any(error.field == 'household_id' for error in errors)

    def test_missing_payer_id_fails_validation(self):
        """Test that missing payer_id fails validation."""
        # Arrange
        validator = BillValidator()
        bill_data = {
            'household_id': 1,
            'title': 'Groceries',
            'amount': 150.00
        }

        # Act
        errors = validator.validate(bill_data)

        # Assert
        assert len(errors) > 0
        assert any(error.field == 'payer_id' for error in errors)

    def test_zero_amount_fails_validation(self):
        """Test that zero amount fails validation."""
        # Arrange
        validator = BillValidator()
        bill_data = {
            'household_id': 1,
            'payer_id': 1,
            'title': 'Free Stuff',
            'amount': 0
        }

        # Act
        errors = validator.validate(bill_data)

        # Assert
        assert len(errors) > 0
        assert any(error.field == 'amount' and 'greater than zero' in error.message for error in errors)

    def test_recurring_bill_without_frequency_fails(self):
        """Test that recurring bill without frequency fails validation."""
        # Arrange
        validator = BillValidator()
        bill_data = {
            'household_id': 1,
            'payer_id': 1,
            'title': 'Monthly Subscription',
            'amount': 9.99,
            'is_recurring': True
        }

        # Act
        errors = validator.validate(bill_data)

        # Assert
        assert len(errors) > 0
        assert any(error.field == 'frequency' for error in errors)

    def test_recurring_bill_with_invalid_frequency_fails(self):
        """Test that recurring bill with invalid frequency fails validation."""
        # Arrange
        validator = BillValidator()
        bill_data = {
            'household_id': 1,
            'payer_id': 1,
            'title': 'Subscription',
            'amount': 15.00,
            'is_recurring': True,
            'frequency': 'yearly'  # Invalid, only monthly/weekly/one-time allowed
        }

        # Act
        errors = validator.validate(bill_data)

        # Assert
        assert len(errors) > 0
        assert any(error.field == 'frequency' for error in errors)