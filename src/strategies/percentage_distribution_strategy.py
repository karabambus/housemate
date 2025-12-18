"""
Percentage Distribution Strategy

SOLID Principles Demonstrated:
- O (Open/Closed): This is one implementation; new strategies can be added without modifying this
- L (Liskov Substitution): This can be substituted for any ICostDistributionStrategy
- S (Single Responsibility): Only handles percentage-based distribution calculation

This strategy splits the bill based on custom percentage shares for each participant.
"""

from typing import List, Dict
from src.interfaces.i_cost_strategy import ICostDistributionStrategy


class PercentageDistributionStrategy(ICostDistributionStrategy):
    """
    Splits costs based on percentage shares specified for each participant.

    Example:
        Total: 200.00
        Participants: [1, 2, 3]
        Distribution Params: {1: 50.0, 2: 30.0, 3: 20.0}  # percentages
        Result: {1: 100.00, 2: 60.00, 3: 40.00}

    SOLID (O): New strategies can be added without modifying this class
    SOLID (L): Can be substituted anywhere ICostDistributionStrategy is expected
    """

    def calculate(self, total_amount: float, participants: List[int],
                  distribution_params: Dict = None) -> Dict[int, float]:
        """
        Calculate percentage-based amounts for each participant.

        Args:
            total_amount: Total bill amount to distribute
            participants: List of user IDs who will share the cost
            distribution_params: Dictionary mapping user_id -> percentage_share

        Returns:
            Dictionary mapping user_id -> amount_owed

        Raises:
            ValueError: If parameters are invalid
        """
        # Validation
        if total_amount < 0:
            raise ValueError("Total amount cannot be negative")

        if not participants or len(participants) == 0:
            raise ValueError("Must have at least one participant")

        if not distribution_params:
            raise ValueError("Distribution parameters must be provided for percentage distribution")

        # Ensure all participants have a percentage specified
        for user_id in participants:
            if user_id not in distribution_params:
                raise ValueError(f"Percentage share not specified for participant {user_id}")

        # Calculate total of percentages
        total_percentage = sum(distribution_params[user_id] for user_id in participants)

        if round(total_percentage, 2) != 100.0:
            raise ValueError("Sum of percentage shares must equal 100")

        # Build result dictionary
        result = {}
        for user_id in participants:
            percentage = distribution_params[user_id]
            amount_owed = round((percentage / 100.0) * total_amount, 2)
            result[user_id] = amount_owed

        return result

    def get_strategy_name(self) -> str:
        """
        Return the name of this distribution strategy.

        Returns:
            Strategy name (e.g., "percentage")
        """
        return "percentage"