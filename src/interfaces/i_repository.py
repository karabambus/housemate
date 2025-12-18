"""
Repository Interface

SOLID Principles Demonstrated:
- I (Interface Segregation): Small, focused interface for data access
- D (Dependency Inversion): Services depend on this abstraction, not concrete implementations

This interface defines the contract for repository pattern.
Concrete implementations (SQLite, PostgreSQL, MongoDB) can be swapped without changing services.
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Any, Dict


class IRepository(ABC):
    """
    Generic repository interface for data access.

    SOLID (I): Focused interface - only CRUD operations
    SOLID (D): High-level modules (services) depend on this, not on SQLiteRepository
    """

    @abstractmethod
    def find_by_id(self, entity_id: int) -> Optional[Any]:
        """
        Find an entity by its ID.

        Args:
            entity_id: The ID of the entity to find

        Returns:
            The entity if found, None otherwise
        """
        pass

    @abstractmethod
    def find_all(self) -> List[Any]:
        """
        Find all entities.

        Returns:
            List of all entities
        """
        pass

    @abstractmethod
    def create(self, **kwargs) -> int:
        """
        Create a new entity.

        Args:
            **kwargs: Entity attributes

        Returns:
            The ID of the newly created entity
        """
        pass

    @abstractmethod
    def update(self, entity_id: int, **kwargs) -> bool:
        """
        Update an existing entity.

        Args:
            entity_id: The ID of the entity to update
            **kwargs: Entity attributes to update

        Returns:
            True if updated successfully, False otherwise
        """
        pass

    @abstractmethod
    def delete(self, entity_id: int) -> bool:
        """
        Delete an entity.

        Args:
            entity_id: The ID of the entity to delete

        Returns:
            True if deleted successfully, False otherwise
        """
        pass


class IBillRepository(IRepository):
    """
    Specialized interface for bill data access.

    SOLID (I): Extends base repository with bill-specific methods
    Demonstrates Interface Segregation - clients only depend on what they need
    """

    @abstractmethod
    def find_by_household(self, household_id: int) -> List[Any]:
        """
        Find all bills for a household.

        Args:
            household_id: The household ID

        Returns:
            List of bills for the household
        """
        pass

    @abstractmethod
    def find_pending_bills(self, user_id: int) -> List[Any]:
        """
        Find all pending bills for a user.

        Args:
            user_id: The user ID

        Returns:
            List of pending bills
        """
        pass
