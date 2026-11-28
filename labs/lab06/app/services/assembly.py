from app.domain.senders import EmailSender, SmsSender, PushSender
from app.services.notification_service import NotificationService
from app.support.types import Outbox



def build_service():
    return NotificationService({"EMAIL": EmailSender(), "SMS": SmsSender(),"PUSH":PushSender()}, Outbox())
