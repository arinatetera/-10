import pytest
from app import api
from app.support.errors import DomainError


def assert_code(code, operation):
    with pytest.raises(DomainError) as error:
        operation()
    assert error.value.code == code

from app.support.types import Recipient, DeliveryReceipt

def test_legacy_mailbox_adapter_is_local():
    from app.domain.notification import Notification
    from app.domain.senders import NotificationSender
    from app.domain.adapters import LegacyMailboxAdapter
    from app.support.types import LegacyMailbox
    mailbox = LegacyMailbox()
    sender = LegacyMailboxAdapter(mailbox)
    assert isinstance(sender, NotificationSender)
    result = sender.send(Notification(Recipient(email="a@example.test"), "OK"))
    assert result == DeliveryReceipt("EMAIL", "a@example.test", "OK")
    assert mailbox.messages == [("a@example.test", "OK")]
    assert_code("MISSING_CONTACT", lambda: sender.send(Notification(Recipient(), "OK")))
    assert len(mailbox.messages) == 1
