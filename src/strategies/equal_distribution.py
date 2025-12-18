"""
Equal Distribution Strategy

SOLID Principles Demonstrated:
- O (Open/Closed): This is one implementation; new strategies can be added without modifying this
- L (Liskov Substitution): This can be substituted for any ICostDistributionStrategy
- S (Single Responsibility): Only handles equal distribution calculation

This strategy splits the bill equally among all participants.
"""

from typing import List, Dict
from src.interfaces.i_cost_strategy import ICostDistributionStrategy


class EqualDistributionStrategy(ICostDistributionStrategy):
    """
    Splits costs equally among all participants.

    Example:
        Total: 300.00
        Participants: [1, 2, 3]
        Result: {1: 100.00, 2: 100.00, 3: 100.00}

    SOLID (O): New strategies can be added without modifying this class
    SOLID (L): Can be substituted anywhere ICostDistributionStrategy is expected
    """

    def calculate(self, total_amount: float, participants: List[int],
                  distribution_params: Dict = None) -> Dict[int, float]:
        """
        Calculate equal split among participants.

        Args:
            total_amount: Total bill amount to distribute
            participants: List of user IDs who will share the cost
            distribution_params: Not used for equal distribution (ignored)

        Returns:
            Dictionary mapping user_id -> equal_amount

        Raises:
            ValueError: If total_amount is negative or participants list is empty
        """
        # Validation
        if total_amount < 0:
            raise ValueError("Total amount cannot be negative")

        if not participants or len(participants) == 0:
            raise ValueError("Must have at least one participant")

        # Calculate equal share
        num_participants = len(participants)
        equal_share = round(total_amount / num_participants, 2)

        # Handle rounding errors: ensure total matches exactly
        # Give any remainder to the first participant
        total_distributed = equal_share * num_participants
        rounding_diff = round(total_amount - total_distributed, 2)

        # Build result dictionary
        result = {}
        for i, user_id in enumerate(participants):
            if i == 0:
                # First participant gets any rounding difference
                result[user_id] = round(equal_share + rounding_diff, 2)
            else:
                result[user_id] = equal_share

        return result

    def get_strategy_name(self) -> str:
        """
        Return the strategy name.

        Returns:
            "equal"
        """
        return "equal"
