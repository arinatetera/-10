class LegacyMailboxAdapter:
    def __init__(self, mailbox):
        self._mailbox = mailbox

    def send(self, notification):
        raise NotImplementedError("Дополнительное задание ЛР5")
