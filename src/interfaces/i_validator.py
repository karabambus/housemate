"""
Validator Interface

SOLID Principles Demonstrated:
- I (Interface Segregation): Small, focused interface for validation only
- S (Single Responsibility): Validators only validate, don't perform business logic

This interface defines the contract for validation logic.
"""

from abc import ABC, abstractmethod
from typing import Dict, List


class ValidationError:
    """
    Represents a validation error.
    """

    def __init__(self, field: str, message: str):
        """
        Initialize validation error.

        Args:
            field: The field that failed validation
            message: The error message
        """
        self.field = field
        self.message = message

    def __repr__(self):
        return f"ValidationError(field='{self.field}', message='{self.message}')"


class IValidator(ABC):
    """
    Interface for validator classes.

    SOLID (I): Small, focused interface - only validation
    SOLID (S): Validators have single responsibility - validate data

    This keeps validation logic separate from business logic and data access.
    """

    @abstractmethod
    def validate(self, data: Dict) -> List[ValidationError]:
        """
        Validate data.

        Args:
            data: Dictionary of data to validate

        Returns:
            List of ValidationError objects (empty if valid)

        Example:
            validator = BillValidator()
            errors = validator.validate({'amount': -10, 'title': ''})
            if errors:
                for error in errors:
                    print(f"{error.field}: {error.message}")
        """
        pass

    def is_valid(self, data: Dict) -> bool:
        """
        Check if data is valid.

        Args:
            data: Dictionary of data to validate

        Returns:
            True if valid, False otherwise
        """
        return len(self.validate(data)) == 0
