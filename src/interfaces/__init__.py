"""
SOLID Interfaces Package

This package contains all the abstract interfaces demonstrating SOLID principles:

- ICostDistributionStrategy: Strategy interface (O, L)
- IRepository, IBillRepository: Repository interfaces (I, D)
- IValidator: Validator interface (I, S)
- INotificationSender, IEmailSender: Notification interfaces (I, D)

SOLID Principles:
- S (Single Responsibility): Each interface has one focused purpose
- O (Open/Closed): Interfaces allow extension without modification
- L (Liskov Substitution): Implementations are substitutable
- I (Interface Segregation): Small, focused interfaces instead of large ones
- D (Dependency Inversion): Depend on abstractions, not concrete classes
"""

from src.interfaces.i_cost_strategy import ICostDistributionStrategy
from src.interfaces.i_repository import IRepository, IBillRepository
from src.interfaces.i_validator import IValidator, ValidationError
from src.interfaces.i_notification import INotificationSender, IEmailSender

__all__ = [
    'ICostDistributionStrategy',
    'IRepository',
    'IBillRepository',
    'IValidator',
    'ValidationError',
    'INotificationSender',
    'IEmailSender',
]
