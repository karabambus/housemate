"""
Bill Service

SOLID Principles Demonstrated:
- S (Single Responsibility): Only coordinates bill operations, doesn't do database/validation itself
- D (Dependency Inversion): Depends on abstractions (interfaces), not concrete implementations

This service coordinates BillRepository, BillValidator, and CostCalculator.
"""

from typing import List, Optional, Dict
from src.models.bill import Bill
from src.interfaces.i_repository import IBillRepository
from src.interfaces.i_validator import IValidator
from src.interfaces.i_cost_strategy import ICostDistributionStrategy
from src.services.cost_calculator import CostCalculator


class BillService:
    """
    Service for managing bill operations.

    SOLID (S): Single responsibility - coordinate bill operations
    SOLID (D): Depends on abstractions via dependency injection
    """

    def __init__(self, repository: IBillRepository, validator: IValidator, calculator: CostCalculator):
        """
        Initialize BillService with dependencies.

        SOLID (D): Dependencies INJECTED via constructor
        - Depends on IBillRepository interface, not BillRepository class
        - Depends on IValidator interface, not BillValidator class
        - Depends on CostCalculator for distribution logic

        Args:
            repository: Bill repository (abstraction)
            validator: Bill validator (abstraction)
            calculator: Cost calculator for distribution strategies
        """
        self.repository = repository
        self.validator = validator
        self.calculator = calculator

    def create_bill(
        self,
        household_id: int,
        payer_id: int,
        title: str,
        amount: float,
        category: str = None,
        is_recurring: bool = False,
        frequency: str = None,
        due_date: str = None
    ) -> int:
        """
        Create a new bill.

        SOLID (S): This method coordinates - validation + repository
        Doesn't do validation itself (delegates to validator)
        Doesn't do database itself (delegates to repository)

        Args:
            household_id: Household ID
            payer_id: User who paid the bill
            title: Bill title
            amount: Bill amount
            category: Bill category (rent, utilities, food, other)
            is_recurring: Whether bill recurs
            frequency: Frequency if recurring (monthly, weekly, one-time)
            due_date: Due date (YYYY-MM-DD format)

        Returns:
            The ID of the newly created bill

        Raises:
            ValueError: If validation fails
        """
        # Step 1: Validate data (delegate to validator)
        data = {
            'household_id': household_id,
            'payer_id': payer_id,
            'title': title,
            'amount': amount,
            'category': category,
            'is_recurring': is_recurring,
            'frequency': frequency
        }

        errors = self.validator.validate(data)
        if errors:
            error_messages = [f"{e.field}: {e.message}" for e in errors]
            raise ValueError(f"Validation failed: {'; '.join(error_messages)}")

        # Step 2: Save to database (delegate to repository)
        bill_id = self.repository.create(
            household_id=household_id,
            payer_id=payer_id,
            title=title,
            amount=amount,
            category=category,
            is_recurring=is_recurring,
            frequency=frequency,
            payment_status='pending',
            due_date=due_date
        )

        return bill_id

    def get_bill(self, bill_id: int) -> Optional[Bill]:
        """
        Get a bill by ID.

        Args:
            bill_id: The bill ID

        Returns:
            Bill if found, None otherwise
        """
        return self.repository.find_by_id(bill_id)

    def get_household_bills(self, household_id: int) -> List[Bill]:
        """
        Get all bills for a household.

        Args:
            household_id: The household ID

        Returns:
            List of bills for the household
        """
        return self.repository.find_by_household(household_id)

    def get_pending_bills(self, user_id: int) -> List[Bill]:
        """
        Get all pending bills for a user.

        Args:
            user_id: The user ID

        Returns:
            List of pending bills
        """
        return self.repository.find_pending_bills(user_id)

    def distribute_bill(
        self,
        bill_id: int,
        strategy: ICostDistributionStrategy,
        participants: List[int],
        distribution_params: Dict = None
    ) -> Dict[int, float]:
        """
        Calculate how to distribute bill costs among participants.

        SOLID (S): Delegates calculation to CostCalculator
        SOLID (O): Can use ANY strategy (Open/Closed Principle)
        SOLID (L): All strategies are substitutable (Liskov)

        Args:
            bill_id: The bill to distribute
            strategy: Distribution strategy to use
            participants: List of user IDs to split among
            distribution_params: Strategy-specific parameters

        Returns:
            Dictionary mapping user_id -> amount_owed

        Example:
            from src.strategies import EqualDistributionStrategy

            service.distribute_bill(
                bill_id=1,
                strategy=EqualDistributionStrategy(),
                participants=[1, 2, 3]
            )
            # Returns: {1: 100.00, 2: 100.00, 3: 100.00}
        """
        # Get the bill
        bill = self.repository.find_by_id(bill_id)
        if not bill:
            raise ValueError(f"Bill {bill_id} not found")

        # Use calculator to determine distribution
        distribution = self.calculator.calculate_with_strategy(
            strategy=strategy,
            total_amount=bill.amount,
            participants=participants,
            distribution_params=distribution_params
        )

        return distribution

    def update_bill_status(self, bill_id: int, status: str) -> bool:
        """
        Update bill payment status.

        Args:
            bill_id: The bill ID
            status: New status (pending, paid, overdue)

        Returns:
            True if updated successfully

        Raises:
            ValueError: If status is invalid
        """
        valid_statuses = ['pending', 'paid', 'overdue']
        if status not in valid_statuses:
            raise ValueError(f"Status must be one of: {', '.join(valid_statuses)}")

        return self.repository.update(bill_id, payment_status=status)

    def delete_bill(self, bill_id: int) -> bool:
        """
        Delete a bill.

        Args:
            bill_id: The bill ID

        Returns:
            True if deleted successfully
        """
        return self.repository.delete(bill_id)
