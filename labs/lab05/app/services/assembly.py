from app.services.notification_service import NotificationService
from app.support.types import Outbox
from app.domain.senders import EmailSender,SmsSender

_shared_outbox = Outbox()


def build_service():
    my_senders = {
        "EMAIL": EmailSender(),
        "SMS": SmsSender()
    }
    my_outbox = Outbox()
    return NotificationService(my_senders, my_outbox)
