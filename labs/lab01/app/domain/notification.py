from app.support.errors import DomainError


# ЛР1: класс Notification
class Notification:
    def __init__(self, recipient, message):
        if not isinstance(message, str):
            raise DomainError("INVALID_MESSAGE")

        message = message.strip()

        if not message:
            raise DomainError("INVALID_MESSAGE")

        self.recipient = recipient
        self.message = message

    def describe(self):
        return f"message={self.message}"

