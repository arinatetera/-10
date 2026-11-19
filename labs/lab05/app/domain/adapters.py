from app.support.types import DeliveryReceipt
class LegacyMailboxAdapter:
    def __init__(self, mailbox):
        self._mailbox = mailbox

    def send(self, notification):
        email = notification.recipient.email
        if email is None or "@" not in email:
            raise DomainError("INVALID_DELIVERY")
        self._mailbox.store(email, notification.message)
        return DeliveryReceipt(
            channel="EMAIL",
            destination=email,
            text=notification.message
        )
