"""
Cost Calculator Service (REFACTORED VERSION - FOLLOWS SOLID)

This is the "AFTER" version demonstrating GOOD design using Strategy Pattern.

SOLID Principles Demonstrated:
- ✓ FOLLOWS Open/Closed (O): New strategies can be added without modifying this class
- ✓ FOLLOWS Single Responsibility (S): This class only coordinates, doesn't know distribution logic
- ✓ FOLLOWS Liskov Substitution (L): All strategies are interchangeable
- ✓ Easy to test: Each strategy tested independently
- ✓ Easy to extend: New strategy = create new class, no changes here

Refactored from if/else chain to Strategy Pattern.
"""

from typing import List, Dict
from src.interfaces.i_cost_strategy import ICostDistributionStrategy


class CostCalculator:
    """
    Calculates cost distribution using Strategy Pattern.

    SOLID (O): Open for extension (add new strategies), closed for modification
    SOLID (S): Single responsibility - coordinate strategies, don't implement them
    SOLID (D): Depends on ICostDistributionStrategy abstraction, not concrete classes

    Usage:
        calculator = CostCalculator()
        strategy = EqualDistributionStrategy()
        result = calculator.calculate_with_strategy(strategy, 300.00, [1, 2, 3])
    """

    def calculate_with_strategy(
        self,
        strategy: ICostDistributionStrategy,
        total_amount: float,
        participants: List[int],
        distribution_params: Dict = None
    ) -> Dict[int, float]:
        """
        Calculate cost distribution using the provided strategy.

        ✓ SOLID (O): Adding new strategy requires ZERO changes to this method!
        ✓ SOLID (L): Any ICostDistributionStrategy implementation works here

        Args:
            strategy: The distribution strategy to use (any ICostDistributionStrategy)
            total_amount: Total bill amount
            participants: List of user IDs
            distribution_params: Strategy-specific parameters

        Returns:
            Dictionary mapping user_id -> amount_owed

        Example:
            # Use equal distribution
            equal = EqualDistributionStrategy()
            result = calculator.calculate_with_strategy(equal, 300, [1, 2, 3])

            # Switch to percentage - NO CODE CHANGES needed!
            percentage = PercentageDistributionStrategy()
            result = calculator.calculate_with_strategy(
                percentage, 300, [1, 2, 3],
                {1: 50.0, 2: 30.0, 3: 20.0}
            )
        """
        # Delegate to strategy - this class doesn't know HOW distribution works
        return strategy.calculate(total_amount, participants, distribution_params)

    def get_strategy_name(self, strategy: ICostDistributionStrategy) -> str:
        """
        Get the name of the current strategy.

        Args:
            strategy: The distribution strategy

        Returns:
            Strategy name
        """
        return strategy.get_strategy_name()
