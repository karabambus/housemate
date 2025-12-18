"""
Bill Validator

SOLID Principle: Single Responsibility (S)
- This class has ONE responsibility: Validate bill data
- Does NOT handle database operations or business logic

SOLID Principle: Interface Segregation (I)
- Implements focused IValidator interface with only validate() method
"""

from typing import Dict, List
from src.interfaces.i_validator import IValidator, ValidationError


class BillValidator(IValidator):
    """
    Validator for Bill data.

    SOLID (S): ONLY responsible for validation logic
    SOLID (I): Implements focused IValidator interface
    """

    # Valid bill categories
    VALID_CATEGORIES = ['rent', 'utilities', 'food', 'other']

    # Valid payment statuses
    VALID_STATUSES = ['pending', 'paid', 'overdue']

    # Valid frequencies for recurring bills
    VALID_FREQUENCIES = ['monthly', 'weekly', 'one-time']

    def validate(self, data: Dict) -> List[ValidationError]:
        """
        Validate Bill data.

        Args:
            data: Dictionary of Bill data to validate

        Returns:
            List of ValidationError objects (empty if valid)
        """
        errors = []

        # Validate title
        title = data.get('title', '').strip()
        if not title:
            errors.append(ValidationError('title', 'Title is required'))
        elif len(title) > 255:
            errors.append(ValidationError('title', 'Title cannot exceed 255 characters'))

        # Validate amount
        amount = data.get('amount')
        if amount is None:
            errors.append(ValidationError('amount', 'Amount is required'))
        elif not isinstance(amount, (int, float)):
            errors.append(ValidationError('amount', 'Amount must be a number'))
        elif amount <= 0:
            errors.append(ValidationError('amount', 'Amount must be greater than zero'))

        # Validate household_id
        household_id = data.get('household_id')
        if not household_id:
            errors.append(ValidationError('household_id', 'Household ID is required'))
        elif not isinstance(household_id, int):
            errors.append(ValidationError('household_id', 'Household ID must be an integer'))

        # Validate payer_id
        payer_id = data.get('payer_id')
        if not payer_id:
            errors.append(ValidationError('payer_id', 'Payer ID is required'))
        elif not isinstance(payer_id, int):
            errors.append(ValidationError('payer_id', 'Payer ID must be an integer'))

        # Validate category (optional)
        category = data.get('category')
        if category and category not in self.VALID_CATEGORIES:
            errors.append(ValidationError(
                'category',
                f"Category must be one of: {', '.join(self.VALID_CATEGORIES)}"
            ))

        # Validate payment_status (optional, defaults to 'pending')
        payment_status = data.get('payment_status', 'pending')
        if payment_status not in self.VALID_STATUSES:
            errors.append(ValidationError(
                'payment_status',
                f"Payment status must be one of: {', '.join(self.VALID_STATUSES)}"
            ))

        # Validate frequency (required if is_recurring is True)
        is_recurring = data.get('is_recurring', False)
        frequency = data.get('frequency')
        if is_recurring:
            if not frequency:
                errors.append(ValidationError('frequency', 'Frequency is required for recurring bills'))
            elif frequency not in self.VALID_FREQUENCIES:
                errors.append(ValidationError(
                    'frequency',
                    f"Frequency must be one of: {', '.join(self.VALID_FREQUENCIES)}"
                ))

        return errors
