from app.domain.notification import Notification
from app.support.errors import DomainError
from app.support.types import DeliveryReceipt, Outbox, contact


CONTACT_GETTERS = {
    "EMAIL": lambda recipient: recipient.email,
    "SMS": lambda recipient: recipient.phone,
}

class NotificationService:
    def __init__(self):
        self._outbox = Outbox()

    def send(self, channel, notification):
        getter = CONTACT_GETTERS.get(channel)
        if getter is None:
            raise DomainError("UNSUPPORTED_CHANNEL")
        destination_value = getter(notification.recipient)

        destination = contact(destination_value)
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
