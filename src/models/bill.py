"""
Bill Model

SOLID Principle: Single Responsibility (S)
- This class has ONE responsibility: Represent a bill entity
- Does NOT handle database operations, validation, or business logic
"""

from datetime import datetime
from typing import Optional


class Bill:
    """
    Represents a bill/expense in the system.

    SOLID (S): Only responsible for holding bill data and simple getter methods
    """

    def __init__(
        self,
        bill_id: int,
        household_id: int,
        payer_id: int,
        title: str,
        amount: float,
        category: Optional[str] = None,
        is_recurring: bool = False,
        frequency: Optional[str] = None,
        payment_status: str = 'pending',
        due_date: Optional[str] = None,
        created_at: Optional[str] = None
    ):
        """
        Initialize a Bill instance.

        Args:
            bill_id: Unique bill identifier
            household_id: ID of household this bill belongs to
            payer_id: ID of user who paid the bill
            title: Bill title/description
            amount: Total bill amount
            category: Bill category (rent, utilities, food, other)
            is_recurring: Whether this is a recurring bill
            frequency: Frequency if recurring (monthly, weekly, one-time)
            payment_status: Payment status (pending, paid, overdue)
            due_date: Due date string (YYYY-MM-DD format)
            created_at: Creation timestamp
        """
        self.bill_id = bill_id
        self.household_id = household_id
        self.payer_id = payer_id
        self.title = title
        self.amount = amount
        self.category = category
        self.is_recurring = is_recurring
        self.frequency = frequency
        self.payment_status = payment_status
        self.due_date = due_date
        self.created_at = created_at

    def is_paid(self) -> bool:
        """
        Check if bill is paid.

        Returns:
            True if payment_status is 'paid', False otherwise
        """
        return self.payment_status == 'paid'

    def is_pending(self) -> bool:
        """
        Check if bill is pending.

        Returns:
            True if payment_status is 'pending', False otherwise
        """
        return self.payment_status == 'pending'

    def is_overdue(self) -> bool:
        """
        Check if bill is overdue.

        Returns:
            True if payment_status is 'overdue', False otherwise
        """
        return self.payment_status == 'overdue'

    def get_category_display(self) -> str:
        """
        Get display-friendly category name.

        Returns:
            Capitalized category name or 'Other' if not set
        """
        if not self.category:
            return 'Other'
        return self.category.capitalize()

    def __repr__(self):
        """String representation for debugging."""
        return (
            f"Bill(id={self.bill_id}, title='{self.title}', "
            f"amount={self.amount}, status='{self.payment_status}')"
        )


class BillDistribution:
    """
    Represents how a bill is distributed among household members.

    SOLID (S): Only responsible for holding distribution data
    """

    def __init__(
        self,
        distribution_id: int,
        bill_id: int,
        user_id: int,
        amount: float,
        percentage: Optional[float] = None,
        distribution_strategy: str = 'equal',
        status: str = 'pending'
    ):
        """
        Initialize a BillDistribution instance.

        Args:
            distribution_id: Unique distribution identifier
            bill_id: ID of the bill being distributed
            user_id: ID of user who owes this amount
            amount: Amount this user owes
            percentage: Percentage share (if using percentage strategy)
            distribution_strategy: Strategy used (equal, percentage, fixed)
            status: Payment status for this distribution (pending, paid)
        """
        self.distribution_id = distribution_id
        self.bill_id = bill_id
        self.user_id = user_id
        self.amount = amount
        self.percentage = percentage
        self.distribution_strategy = distribution_strategy
        self.status = status

    def is_paid(self) -> bool:
        """
        Check if this distribution is paid.

        Returns:
            True if status is 'paid', False otherwise
        """
        return self.status == 'paid'

    def __repr__(self):
        """String representation for debugging."""
        return (
            f"BillDistribution(id={self.distribution_id}, user_id={self.user_id}, "
            f"amount={self.amount}, strategy='{self.distribution_strategy}')"
        )
