from app.support.types import Recipient
from app.support.errors import DomainError


class Notification:
    def __init__(self, recipient: Recipient, message: str):
        message = message.strip()

        if not message:
            raise DomainError("INVALID_MESSAGE")

        self._recipient = recipient
        self._message = message

    @property
    def recipient(self):
        return self._recipient

    @property
    def message(self):
        return self._message
