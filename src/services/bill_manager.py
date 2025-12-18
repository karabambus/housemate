"""
Bill Manager (INITIAL VERSION - VIOLATES SOLID)

This is the "BEFORE" version demonstrating POOR design.

SOLID Violations:
- ❌ VIOLATES Single Responsibility (S): This class has MULTIPLE responsibilities:
  1. Database operations (repository responsibility)
  2. Validation logic (validator responsibility)
  3. Business logic coordination (service responsibility)
- ❌ Hard to test: Must mock database AND test validation in same class
- ❌ Hard to maintain: Changes to validation require touching database code
- ❌ Hard to reuse: Can't use validation logic without database dependency

This will be refactored to follow SRP in the next commit.
"""

from typing import List, Optional, Dict
from src.models.bill import Bill


class BillManager:
    """
    Manages all bill operations.

    WARNING: This design violates Single Responsibility Principle!
    This ONE class does TOO MANY things!
    """

    def __init__(self, db):
        """
        Initialize BillManager.

        Args:
            db: DatabaseConnection instance
        """
        self.db = db

    # ========================================================================
    # RESPONSIBILITY 1: DATABASE OPERATIONS (Should be in BillRepository)
    # ========================================================================

    def find_by_id(self, bill_id: int) -> Optional[Bill]:
        """
        Find bill by ID.

        ❌ PROBLEM: This is repository responsibility, not manager responsibility
        """
        query = "SELECT * FROM bills WHERE bill_id = ?"
        results = self.db.execute_query(query, (bill_id,))

        if results:
            row = results[0]
            return Bill(
                bill_id=row['bill_id'],
                household_id=row['household_id'],
                payer_id=row['payer_id'],
                title=row['title'],
                amount=row['amount'],
                category=row['category'],
                is_recurring=bool(row['is_recurring']),
                frequency=row['frequency'],
                payment_status=row['payment_status'],
                due_date=row['due_date'],
                created_at=row['created_at']
            )
        return None

    def find_by_household(self, household_id: int) -> List[Bill]:
        """
        Find all bills for a household.

        ❌ PROBLEM: This is repository responsibility
        """
        query = "SELECT * FROM bills WHERE household_id = ? ORDER BY created_at DESC"
        results = self.db.execute_query(query, (household_id,))

        bills = []
        for row in results:
            bills.append(Bill(
                bill_id=row['bill_id'],
                household_id=row['household_id'],
                payer_id=row['payer_id'],
                title=row['title'],
                amount=row['amount'],
                category=row['category'],
                is_recurring=bool(row['is_recurring']),
                frequency=row['frequency'],
                payment_status=row['payment_status'],
                due_date=row['due_date'],
                created_at=row['created_at']
            ))
        return bills

    # ========================================================================
    # RESPONSIBILITY 2: VALIDATION LOGIC (Should be in BillValidator)
    # ========================================================================

    def validate_bill_data(self, data: Dict) -> List[str]:
        """
        Validate bill data.

        ❌ PROBLEM: This is validator responsibility, not manager responsibility
        Returns list of error messages
        """
        errors = []

        # Validate title
        title = data.get('title', '').strip()
        if not title:
            errors.append("Title is required")
        elif len(title) > 255:
            errors.append("Title cannot exceed 255 characters")

        # Validate amount
        amount = data.get('amount')
        if amount is None:
            errors.append("Amount is required")
        elif not isinstance(amount, (int, float)):
            errors.append("Amount must be a number")
        elif amount <= 0:
            errors.append("Amount must be greater than zero")

        # Validate household_id
        household_id = data.get('household_id')
        if not household_id:
            errors.append("Household ID is required")

        # Validate payer_id
        payer_id = data.get('payer_id')
        if not payer_id:
            errors.append("Payer ID is required")

        # Validate category
        category = data.get('category')
        if category:
            valid_categories = ['rent', 'utilities', 'food', 'other']
            if category not in valid_categories:
                errors.append(f"Category must be one of: {', '.join(valid_categories)}")

        return errors

    # ========================================================================
    # RESPONSIBILITY 3: BUSINESS LOGIC (This is the ONLY thing it should do)
    # ========================================================================

    def create_bill(self, household_id: int, payer_id: int, title: str,
                   amount: float, category: str = None, is_recurring: bool = False,
                   frequency: str = None, due_date: str = None) -> int:
        """
        Create a new bill.

        ❌ PROBLEM: This method mixes validation AND database operations
        """
        # Validation (should be separate)
        data = {
            'household_id': household_id,
            'payer_id': payer_id,
            'title': title,
            'amount': amount,
            'category': category
        }
        errors = self.validate_bill_data(data)
        if errors:
            raise ValueError(f"Validation failed: {'; '.join(errors)}")

        # Database operation (should be separate)
        query = """
            INSERT INTO bills
            (household_id, payer_id, title, amount, category, is_recurring, frequency, payment_status, due_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, 'pending', ?)
        """
        bill_id = self.db.execute_insert(
            query,
            (household_id, payer_id, title, amount, category,
             1 if is_recurring else 0, frequency, due_date)
        )
        return bill_id

    def update_bill_status(self, bill_id: int, status: str) -> bool:
        """
        Update bill payment status.

        ❌ PROBLEM: Validation + database operation mixed together
        """
        # Validation (should be separate)
        valid_statuses = ['pending', 'paid', 'overdue']
        if status not in valid_statuses:
            raise ValueError(f"Status must be one of: {', '.join(valid_statuses)}")

        # Database operation (should be separate)
        query = "UPDATE bills SET payment_status = ? WHERE bill_id = ?"
        rows_affected = self.db.execute_update(query, (status, bill_id))
        return rows_affected > 0

    def delete_bill(self, bill_id: int) -> bool:
        """
        Delete a bill.

        ❌ PROBLEM: This is repository responsibility
        """
        query = "DELETE FROM bills WHERE bill_id = ?"
        rows_affected = self.db.execute_update(query, (bill_id,))
        return rows_affected > 0
