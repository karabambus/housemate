"""
Fixed Amount Distribution Strategy

SOLID Principles Demonstrated:
- O (Open/Closed): This is one implementation; new strategies can be added without modifying this
- L (Liskov Substitution): This can be substituted for any ICostDistributionStrategy
- S (Single Responsibility): Only handles fixed amount distribution calculation

This strategy uses custom fixed amounts for each participant.
Each person pays based on their specific contribution (e.g., groceries where people bought different items).
If fixed amounts don't match the total exactly, they're scaled proportionally.
"""

from typing import List, Dict
from src.interfaces.i_cost_strategy import ICostDistributionStrategy


class FixedDistributionStrategy(ICostDistributionStrategy):
    """
    Splits costs based on fixed amounts specified for each participant.

    The fixed amounts represent desired/intended contributions. If they don't match
    the total exactly (e.g., due to discounts), they're scaled proportionally.

    Example 1 (exact match):
        Total: 380.00
        Participants: [1, 2, 3]
        Distribution Params: {1: 100.00, 2: 150.00, 3: 130.00}  # sum = 380
        Result: {1: 100.00, 2: 150.00, 3: 130.00}

    Example 2 (scaling down):
        Total: 270.00
        Participants: [1, 2, 3]
        Distribution Params: {1: 100.00, 2: 150.00, 3: 50.00}  # sum = 300
        Result: {1: 90.00, 2: 135.00, 3: 45.00}  # scaled proportionally

    SOLID (O): New strategies can be added without modifying this class
    SOLID (L): Can be substituted anywhere ICostDistributionStrategy is expected
    """

    def calculate(self, total_amount: float, participants: List[int],
                  distribution_params: Dict = None) -> Dict[int, float]:
        """
        Calculate fixed amounts for each participant, scaled to match total.

        Args:
            total_amount: Total bill amount to distribute
            participants: List of user IDs who will share the cost
            distribution_params: Dictionary mapping user_id -> fixed_amount

        Returns:
            Dictionary mapping user_id -> amount_owed (scaled if necessary)

        Raises:
            ValueError: If parameters are invalid or fixed amounts can't cover total
        """
        # Validation
        if total_amount < 0:
            raise ValueError("Total amount cannot be negative")

        if not participants or len(participants) == 0:
            raise ValueError("Must have at least one participant")

        if not distribution_params:
            raise ValueError("Distribution parameters must be provided for fixed distribution")

        # Ensure all participants have a fixed amount specified
        for user_id in participants:
            if user_id not in distribution_params:
                raise ValueError(f"Fixed amount not specified for participant {user_id}")

        # Calculate total of fixed amounts
        total_fixed = sum(distribution_params[user_id] for user_id in participants)

        # Fixed amounts must be able to cover the total
        if round(total_fixed, 2) < round(total_amount, 2):
            raise ValueError(
                f"Sum of fixed amounts ({total_fixed:.2f}) cannot cover "
                f"total amount ({total_amount:.2f})"
            )

        # Calculate proportional amounts
        # Each person pays: (their_fixed_amount / total_fixed) * actual_total
        # This handles both exact matches and scaling down for discounts
        result = {}
        for user_id in participants:
            proportional_amount = (distribution_params[user_id] / total_fixed) * total_amount
            result[user_id] = round(proportional_amount, 2)

        return result

    def get_strategy_name(self) -> str:
        """
        Return the name of this distribution strategy.

        Returns:
            Strategy name "fixed"
        """
        return "fixed"
