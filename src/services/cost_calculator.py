"""
Cost Calculator Service (INITIAL VERSION - VIOLATES SOLID)

This is the "BEFORE" version demonstrating POOR design.

SOLID Violations:
- ❌ VIOLATES Open/Closed (O): Adding new strategy requires MODIFYING this class
- ❌ VIOLATES Single Responsibility (S): This class knows ALL distribution logic
- ❌ Hard to test: Must test all strategies in one class
- ❌ Hard to extend: New strategy = modify calculate() method

This will be refactored to follow SOLID principles in the next commit.
"""

from typing import List, Dict


class CostCalculator:
    """
    Calculates cost distribution for bills.

    WARNING: This design violates Open/Closed Principle!
    """

    def calculate(self, strategy_type: str, total_amount: float,
                  participants: List[int], distribution_params: Dict = None) -> Dict[int, float]:
        """
        Calculate how much each participant owes.

        PROBLEM: Uses if/else chain - adding new strategy requires modifying this method!

        Args:
            strategy_type: "equal", "percentage", or "fixed"
            total_amount: Total bill amount
            participants: List of user IDs
            distribution_params: Strategy-specific parameters

        Returns:
            Dictionary mapping user_id -> amount_owed
        """
        # ❌ VIOLATION: if/else chain for each strategy type
        # Adding "weighted" or "income-based" strategy requires CHANGING this code!

        if strategy_type == "equal":
            # Equal distribution logic
            num_participants = len(participants)
            equal_share = round(total_amount / num_participants, 2)
            total_distributed = equal_share * num_participants
            rounding_diff = round(total_amount - total_distributed, 2)

            result = {}
            for i, user_id in enumerate(participants):
                if i == 0:
                    result[user_id] = round(equal_share + rounding_diff, 2)
                else:
                    result[user_id] = equal_share
            return result

        elif strategy_type == "percentage":
            # Percentage distribution logic
            if not distribution_params:
                raise ValueError("Percentages required for percentage distribution")

            total_percentage = sum(distribution_params[user_id] for user_id in participants)
            if round(total_percentage, 2) != 100.0:
                raise ValueError("Percentages must sum to 100")

            result = {}
            for user_id in participants:
                percentage = distribution_params[user_id]
                result[user_id] = round((percentage / 100.0) * total_amount, 2)
            return result

        elif strategy_type == "fixed":
            # Fixed amount distribution logic
            if not distribution_params:
                raise ValueError("Fixed amounts required for fixed distribution")

            total_fixed = sum(distribution_params[user_id] for user_id in participants)
            if round(total_fixed, 2) != round(total_amount, 2):
                raise ValueError("Fixed amounts must equal total")

            result = {}
            for user_id in participants:
                result[user_id] = round(distribution_params[user_id], 2)
            return result

        else:
            raise ValueError(f"Unknown strategy type: {strategy_type}")
