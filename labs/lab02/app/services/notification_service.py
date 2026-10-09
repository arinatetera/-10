from app.domain.notification import Notification
from app.support.errors import DomainError
from app.support.types import DeliveryReceipt, Outbox, contact


class NotificationService:
    def __init__(self):
        self._outbox = Outbox()

    def send(self, channel: str, notification: Notification) -> DeliveryReceipt:
        if channel == "EMAIL":
            destination = notification.recipient.email
        elif channel == "SMS":
            destination = notification.recipient.phone
        else:
            raise DomainError("UNSUPPORTED_CHANNEL")
        receipt = DeliveryReceipt(channel, destination, notification.message)
        self._outbox.add(receipt)
        return receipt

    def sent(self) -> tuple[DeliveryReceipt, ...]:
        return self._outbox.all()


def new_service():
    return NotificationService()


def send_message(service, channel, recipient, message):
    return service.send(channel, Notification(recipient, message))


def sent_messages(service):
    return service.sent()
