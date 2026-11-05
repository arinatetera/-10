from abc import ABC, abstractmethod
from app.domain.notification import Notification
from app.support.types import DeliveryReceipt, contact


class NotificationSender(ABC):
    @abstractmethod
    def send(self, notification: Notification) -> DeliveryReceipt:
        """Сформировать квитанцию, не добавляя её в outbox."""
        raise NotImplementedError


class EmailSender(NotificationSender):
    def send(self, notification: Notification) -> DeliveryReceipt:
        destination = contact(notification.recipient.email)
        return DeliveryReceipt("EMAIL", destination, notification.message)


class SmsSender(NotificationSender):
    def send(self, notification: Notification) -> DeliveryReceipt:
        destination = contact(notification.recipient.phone)
        return DeliveryReceipt("SMS", destination, notification.message)
