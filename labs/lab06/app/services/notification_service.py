from collections.abc import Mapping
from app.domain.notification import Notification
from app.domain.senders import NotificationSender
from app.support.errors import DomainError
from app.support.types import DeliveryReceipt, Outbox, validate_receipt


class NotificationService:
    def __init__(self, senders: Mapping[str, NotificationSender], outbox: Outbox):
        self._senders = dict(senders)
        self._outbox = outbox

    def send(self, channel: str, notification: Notification) -> DeliveryReceipt:
        sender = self._senders.get(channel)
        if sender is None:
            raise DomainError("UNSUPPORTED_CHANNEL")
        receipt = sender.send(notification)
        validate_receipt(receipt, channel)
        self._outbox.add(receipt)
        return receipt

    def sent(self) -> tuple[DeliveryReceipt, ...]:
        return self._outbox.all()


def send_message(service, channel, recipient, message):
    return service.send(channel, Notification(recipient, message))


def sent_messages(service):
    return service.sent()
