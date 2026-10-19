from app.domain.notification import Notification
from app.support.errors import DomainError
from app.support.types import DeliveryReceipt, Outbox, contact


class NotificationService:
    def __init__(self):
        self._outbox = Outbox()

    def send(self, channel: str, notification: Notification) -> DeliveryReceipt:
        raise NotImplementedError("ЛР3: реализуйте NotificationService.send по TASK.md")

    def sent(self) -> tuple[DeliveryReceipt, ...]:
        return self._outbox.all()


def new_service():
    return NotificationService()


def send_message(service, channel, recipient, message):
    return service.send(channel, Notification(recipient, message))


def sent_messages(service):
    return service.sent()
