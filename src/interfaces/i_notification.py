"""
Notification Interface

SOLID Principles Demonstrated:
- I (Interface Segregation): Small, focused interface for notifications only
- D (Dependency Inversion): Services depend on this abstraction, not EmailSender

This interface defines the contract for notification senders.
Different implementations (Email, SMS, Push) can be swapped without changing services.
"""

from abc import ABC, abstractmethod
from typing import List


class INotificationSender(ABC):
    """
    Interface for sending notifications to users.

    SOLID (I): Small interface - only send() method
    SOLID (D): BillService depends on this interface, not concrete EmailSender

    This allows swapping notification methods (email -> SMS -> push) without
    changing the BillService code.
    """

    @abstractmethod
    def send(self, recipient: str, subject: str, message: str) -> bool:
        """
        Send a notification.

        Args:
            recipient: Recipient identifier (email, phone number, user ID, etc.)
            subject: Notification subject
            message: Notification message

        Returns:
            True if sent successfully, False otherwise
        """
        pass


class IEmailSender(INotificationSender):
    """
    Specialized interface for email notifications.

    SOLID (I): Extends base notification with email-specific features
    """

    @abstractmethod
    def send_bulk(self, recipients: List[str], subject: str, message: str) -> int:
        """
        Send email to multiple recipients.

        Args:
            recipients: List of email addresses
            subject: Email subject
            message: Email message

        Returns:
            Number of successfully sent emails
        """
        pass
