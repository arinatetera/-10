from app.domain.notification import Notification
from app.support.types import DeliveryReceipt


class NotificationSender:
    # ЛР3: оформить ABC и общий контракт.
    def send(self, notification: Notification) -> DeliveryReceipt:
        return None


class EmailSender(NotificationSender):
    # ЛР3: перенести сюда существующее EMAIL-поведение.
    pass


class SmsSender(NotificationSender):
    # ЛР3: перенести сюда существующее SMS-поведение.
    pass
