"""
Cost Distribution Strategy Interface

SOLID Principles Demonstrated:
- O (Open/Closed): New distribution strategies can be added without modifying existing code
- L (Liskov Substitution): Any strategy implementation can be substituted at runtime
- I (Interface Segregation): Small, focused interface with single method

This interface defines the contract for cost distribution strategies.
Different implementations (equal, percentage, fixed) can be swapped at runtime.
"""

from abc import ABC, abstractmethod
from typing import List, Dict


class ICostDistributionStrategy(ABC):
    """
    Interface for cost distribution strategies.

    Each strategy calculates how to split a bill amount among participants.

    SOLID (O): To add new strategy (e.g., weighted by income), just create new class
    SOLID (L): All implementations must be substitutable without breaking the system
    SOLID (I): Interface has only ONE method - very focused responsibility
    """

    @abstractmethod
    def calculate(self, total_amount: float, participants: List[int],
                  distribution_params: Dict = None) -> Dict[int, float]:
        """
        Calculate how much each participant owes.

        Args:
            total_amount: Total bill amount to distribute
            participants: List of user IDs who will share the cost
            distribution_params: Strategy-specific parameters (percentages, fixed amounts, etc.)

        Returns:
            Dictionary mapping user_id -> amount_owed

        Example:
            {
                1: 100.00,  # User 1 owes 100.00
                2: 150.00,  # User 2 owes 150.00
                3: 150.00   # User 3 owes 150.00
            }

        Raises:
            ValueError: If parameters are invalid
        """
        pass

    @abstractmethod
    def get_strategy_name(self) -> str:
        """
        Return the name of this distribution strategy.

        Returns:
            Strategy name (e.g., "equal", "percentage", "fixed")
        """
        pass
