from app.domain.notification import Notification
from app.support.errors import DomainError
from app.support.types import DeliveryReceipt, Outbox, contact


class NotificationService:
    def __init__(self):
        self.outbox = Outbox()

    def send(self, channel, notification):
        if channel == "EMAIL":
            destination = contact(notification.recipient.email)
        elif channel == "SMS":
            destination = contact(notification.recipient.phone)
        else:
            raise DomainError("UNSUPPORTED_CHANNEL")

        receipt = DeliveryReceipt(
            channel,
            destination,
            notification.message
        )

        self.outbox.add(receipt)
        return receipt

    def sent(self):
        return self.outbox.all()


def new_service():
    return NotificationService()


def send_message(service, channel, recipient, message):
    notification = Notification(recipient, message)
    return service.send(channel, notification)


def sent_messages(service):
    return service.sent()
