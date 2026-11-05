from app.domain.notification import Notification
from app.domain.senders import EmailSender, SmsSender
from app.support.errors import DomainError
from app.support.types import DeliveryReceipt, Outbox, validate_receipt


class NotificationService(EmailSender):
    # ЛР4: сервис не является разновидностью EMAIL-отправителя.
    def __init__(self):
        self._sms = SmsSender()
        self._outbox = Outbox()

    def send(self, channel: str, notification: Notification) -> DeliveryReceipt:
        if channel == "EMAIL":
            if not notification.message.strip():
                raise DomainError("INVALID_MESSAGE")
            receipt = EmailSender.send(self, notification)
        elif channel == "SMS":
            if not notification.message.strip():
                raise DomainError("INVALID_MESSAGE")
            receipt = self._sms.send(notification)
        else:
            raise DomainError("UNSUPPORTED_CHANNEL")
        validate_receipt(receipt, channel)
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


def diagnostic(notification):
    return f"message={notification.message}"
