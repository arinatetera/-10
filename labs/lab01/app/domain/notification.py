# ЛР1: определите здесь класс Notification.
class Notification:
    def __init__(self, recipient, message):
        self.recipient = recipient
        self.message = message.strip()

    def describe(self):
        return f"message={self.message}"
