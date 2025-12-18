"""
Cost Distribution Strategies Package

This package contains all cost distribution strategy implementations
demonstrating the Strategy Pattern (Open/Closed and Liskov Substitution principles).

Available Strategies:
- EqualDistributionStrategy: Split equally among all participants
- PercentageDistributionStrategy: Split by custom percentages
- FixedDistributionStrategy: Each participant pays a specific fixed amount

SOLID Principles Demonstrated:
- O (Open/Closed): New strategies can be added without modifying existing code
- L (Liskov Substitution): All strategies are interchangeable at runtime
- S (Single Responsibility): Each strategy does ONE thing - calculate distribution
"""

from src.strategies.equal_distribution import EqualDistributionStrategy
from src.strategies.percentage_distribution_strategy import PercentageDistributionStrategy
from src.strategies.fixed_distribution_strategy import FixedDistributionStrategy

__all__ = [
    'EqualDistributionStrategy',
    'PercentageDistributionStrategy',
    'FixedDistributionStrategy',
]
