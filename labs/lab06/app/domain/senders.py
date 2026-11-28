from app.support.errors import DomainError
from app.support.types import validate_receipt
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


class PushSender(NotificationSender):
    def send(self, notification: Notification) -> DeliveryReceipt:
        destination = contact(notification.recipient.push_token)
        return DeliveryReceipt("PUSH", destination, notification.message)


class TaggedSender(NotificationSender):
    """Добавляет метку к результату выбранного отправителя, не меняя сообщение."""

    def __init__(self, sender, prefix):
        raise NotImplementedError("ЛР6: реализуйте TaggedSender.__init__ по TASK.md")

    def send(self, notification):
        raise NotImplementedError("ЛР6: реализуйте TaggedSender.send по TASK.md")


class SuffixSender(NotificationSender):
    def __init__(self, sender, suffix):
        raise NotImplementedError("ЛР6: реализуйте SuffixSender.__init__ по TASK.md")

    def send(self, notification):
        raise NotImplementedError("ЛР6: реализуйте SuffixSender.send по TASK.md")
