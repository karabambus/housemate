import pytest
from src.models.bill import Bill


class TestBillModel:

    def test_bill_creation(self):
        bill = Bill(
            bill_id=1,
            household_id=10,
            payer_id=5,
            title='Test Bill',
            amount=100.0,
            category='utilities',
            is_recurring=False,
            frequency=None,
            payment_status='pending',
            due_date='2024-12-31',
            created_at='2024-01-01 10:00:00'
        )

        assert bill.bill_id == 1
        assert bill.title == 'Test Bill'
        assert bill.amount == 100.0
        assert bill.is_recurring is False


    def test_bill_str_representation(self):
        bill = Bill(
            bill_id=1,
            household_id=10,
            payer_id=5,
            title='Groceries',
            amount=75.50,
            category='food',
            payment_status='pending'
        )

        str_repr = str(bill)
        assert 'Groceries' in str_repr
        assert '75.5' in str_repr

    def test_bill_repr(self):
        bill = Bill(
            bill_id=5,
            household_id=10,
            payer_id=3,
            title='Internet',
            amount=60.0,
            category='utilities',
            payment_status='pending'
        )

        repr_str = repr(bill)
        assert 'Bill' in repr_str
        assert 'Internet' in repr_str
