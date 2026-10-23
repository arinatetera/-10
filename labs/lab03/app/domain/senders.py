from abc import ABC, abstractmethod

from app.domain.notification import Notification
from app.support.errors import DomainError
from app.support.types import DeliveryReceipt, contact


class NotificationSender(ABC):
    @abstractmethod
    def send(self, notification: Notification) -> DeliveryReceipt:
        pass


class EmailSender(NotificationSender):
    def __init__(self, prefix: str = ""):
        self.prefix = prefix

    def send(self, notification: Notification) -> DeliveryReceipt:
        destination = contact(notification.recipient.email)
        return DeliveryReceipt(
            "EMAIL",
            destination,
            self.prefix + notification.message,)


class SmsSender(NotificationSender):
    def send(self, notification: Notification) -> DeliveryReceipt:
        destination = contact(notification.recipient.phone)
        return DeliveryReceipt(
            "SMS",
            destination,
            notification.message,)

class TgSender(NotificationSender):
    def send(self, notification: Notification) -> DeliveryReceipt:
        destination = contact(notification.recipient.phone)
        return DeliveryReceipt(
            "TG",
            destination,
            notification.message,)