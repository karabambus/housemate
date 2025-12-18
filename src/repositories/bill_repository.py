"""
Bill Repository

SOLID Principle: Single Responsibility (S)
- This class has ONE responsibility: Database access for bills
- Does NOT handle validation or business logic

SOLID Principle: Dependency Inversion (D)
- Services depend on IBillRepository interface, not this concrete implementation
"""

from typing import List, Optional
from src.models.bill import Bill
from src.interfaces.i_repository import IBillRepository


class BillRepository(IBillRepository):
    """
    Repository for accessing Bill data from database.

    SOLID (S): ONLY responsible for database operations
    SOLID (D): Implements IBillRepository abstraction
    """

    def __init__(self, db):
        """
        Initialize repository with database connection.

        Args:
            db: DatabaseConnection instance (dependency injection)
        """
        self.db = db

    def find_by_id(self, bill_id: int) -> Optional[Bill]:
        """
        Find bill by ID.

        Args:
            bill_id: The bill ID

        Returns:
            Bill if found, None otherwise
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

    def find_all(self) -> List[Bill]:
        """
        Find all bills.

        Returns:
            List of all bills
        """
        query = "SELECT * FROM bills ORDER BY created_at DESC"
        results = self.db.execute_query(query)

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

    def find_by_household(self, household_id: int) -> List[Bill]:
        """
        Find all bills for a household.

        Args:
            household_id: The household ID

        Returns:
            List of bills for the household
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

    def find_pending_bills(self, user_id: int) -> List[Bill]:
        """
        Find all pending bills for a user.

        Args:
            user_id: The user ID

        Returns:
            List of pending bills
        """
        query = """
            SELECT b.* FROM bills b
            JOIN bill_distributions bd ON b.bill_id = bd.bill_id
            WHERE bd.user_id = ? AND bd.status = 'pending'
            ORDER BY b.due_date ASC
        """
        results = self.db.execute_query(query, (user_id,))

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

    def create(self, **kwargs) -> int:
        """
        Create a new bill.

        Args:
            **kwargs: Bill attributes (household_id, payer_id, title, amount, etc.)

        Returns:
            The ID of the newly created bill
        """
        query = """
            INSERT INTO bills
            (household_id, payer_id, title, amount, category, is_recurring, frequency, payment_status, due_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        bill_id = self.db.execute_insert(
            query,
            (
                kwargs['household_id'],
                kwargs['payer_id'],
                kwargs['title'],
                kwargs['amount'],
                kwargs.get('category'),
                1 if kwargs.get('is_recurring', False) else 0,
                kwargs.get('frequency'),
                kwargs.get('payment_status', 'pending'),
                kwargs.get('due_date')
            )
        )
        return bill_id

    def update(self, bill_id: int, **kwargs) -> bool:
        """
        Update an existing bill.

        Args:
            bill_id: The bill ID
            **kwargs: Bill attributes to update

        Returns:
            True if updated successfully
        """
        query = """
            UPDATE bills
            SET payment_status = ?
            WHERE bill_id = ?
        """
        rows_affected = self.db.execute_update(
            query,
            (kwargs.get('payment_status', 'pending'), bill_id)
        )
        return rows_affected > 0

    def delete(self, bill_id: int) -> bool:
        """
        Delete a bill.

        Args:
            bill_id: The bill ID

        Returns:
            True if deleted successfully
        """
        query = "DELETE FROM bills WHERE bill_id = ?"
        rows_affected = self.db.execute_update(query, (bill_id,))
        return rows_affected > 0
