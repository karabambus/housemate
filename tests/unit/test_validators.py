from src.validators.bill_validator import BillValidator


class TestBillValidator:

    def test_valid_bill_passes_validation(self):
        validator = BillValidator()
        bill_data = {
            'title': 'Electricity Bill',
            'amount': 120.50,
            'due_date': '2024-12-01'
        }
        errors = validator.validate(bill_data)
        assert not errors
        pass

    def test_missing_title_fails_validation(self):
        validator = BillValidator()
        bill_data = {
            'amount': 75.00,
            'due_date': '2024-11-15'
        }
        errors = validator.validate(bill_data)
        assert 'title' in errors
        pass

    def test_negative_amount_fails_validation(self):
        validator = BillValidator()
        bill_data = {
            'title': 'Water Bill',
            'amount': -50.00,
            'due_date': '2024-10-10'
        }
        errors = validator.validate(bill_data)
        assert 'amount' in errors
        pass

    def test_invalid_category_fails_validation(self):
        validator = BillValidator()
        bill_data = {
            'title': 'Internet Bill',
            'amount': 60.00,
            'due_date': '2024-09-20',
            'category': 'invalid_category'
        }
        errors = validator.validate(bill_data)
        assert 'category' in errors
        pass