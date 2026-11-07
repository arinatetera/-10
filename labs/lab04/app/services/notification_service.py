from app.domain.notification import Notification
from app.domain.senders import EmailSender, SmsSender, TgSender
from app.support.errors import DomainError
from app.support.types import DeliveryReceipt, Outbox, validate_receipt


class NotificationService:
    #сервис не является разновидностью EMAIL-отправителя.
    def __init__(self):
        self._senders = {
            "EMAIL": EmailSender(),
            "SMS": SmsSender(),
            "TG": TgSender()
        }
        self._outbox = Outbox()

    def send(self, channel: str, notification: Notification) -> DeliveryReceipt:
        # 1. Проверяем, есть ли такой канал в нашем словаре
        if channel not in self._senders:
            raise DomainError("UNSUPPORTED_CHANNEL")

        # 2. Получаем нужного отправителя
        sender = self._senders[channel]

        # 3. Отправляем. Проверки текста тут больше нет (она в Notification).
        # Проверка контакта произойдет внутри метода send() отправителя.
        receipt = sender.send(notification)

        # 4. Валидация и запись
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
