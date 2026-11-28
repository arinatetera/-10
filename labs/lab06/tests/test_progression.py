import pytest
from datetime import date, datetime, timezone
from decimal import Decimal
from app import api
from app.support.errors import DomainError


def code(expected, operation):
    with pytest.raises(DomainError) as caught:
        operation()
    assert caught.value.code == expected

from app.domain.notification import Notification
from app.domain.senders import EmailSender, SmsSender
from app.support.types import Recipient, DeliveryReceipt

@pytest.mark.parametrize("sender,good,bad", [
 (EmailSender, Recipient(email="a@test"), Recipient(phone="123")),
 (SmsSender, Recipient(phone="123"), Recipient(email="a@test"))])
def test_progression_sender_success_error_success(sender, good, bad):
    sender = sender()
    first = sender.send(Notification(good, "FIRST"))
    code("MISSING_CONTACT", lambda: sender.send(Notification(bad, "FAILED")))
    third = sender.send(Notification(good, "THIRD"))
    assert isinstance(first, DeliveryReceipt) and isinstance(third, DeliveryReceipt)
    assert (first.text, third.text) == ("FIRST", "THIRD")

def test_progression_failed_send_is_not_recorded():
    service = api.create()
    first = api.send(service, "EMAIL", Recipient(email="a@test"), "FIRST")
    before = api.sent(service)
    code("MISSING_CONTACT", lambda: api.send(service, "EMAIL", Recipient(phone="1"), "FAILED"))
    assert api.sent(service) == before
    third = api.send(service, "EMAIL", Recipient(email="c@test"), "THIRD")
    assert api.sent(service) == (first, third)
    assert first.destination == "a@test" and third.destination == "c@test"

from app.domain.senders import NotificationSender
from app.services.notification_service import NotificationService
from app.support.types import Outbox

def test_progression_sender_error_has_no_phantom_receipt():
    calls = []
    class Once(NotificationSender):
        def __bool__(self): return False
        def send(self, item):
            calls.append(item)
            if len(calls) == 1: raise DomainError("TEMPORARY")
            return DeliveryReceipt("EMAIL", "a@test", item.message)
    senders = {"EMAIL": Once()}
    outbox = Outbox()
    service = NotificationService(senders, outbox)
    senders.clear()
    item = Notification(Recipient(email="a@test"), "OK")
    code("TEMPORARY", lambda: service.send("EMAIL", item))
    assert len(calls) == 1 and outbox.all() == ()
    receipt = service.send("EMAIL", item)
    assert outbox.all() == (receipt,) and calls == [item, item]

from app.domain.senders import TaggedSender, PushSender
from app.services.notification_service import NotificationService
from app.support.types import Outbox

def test_progression_tagged_sender_preserves_message_and_journal():
    item = Notification(Recipient(push_token="device"), "OK")
    wrapped = TaggedSender(TaggedSender(PushSender(), "B:"), "A:")
    service = NotificationService({"PUSH": wrapped}, Outbox())
    result = service.send("PUSH", item)
    assert result.text == "A:B:OK" and result.destination == "device"
    assert item.message == "OK" and service.sent() == (result,)
    assert TaggedSender(PushSender(), "").send(item).text == "OK"
    code("MISSING_CONTACT", lambda: service.send("PUSH", Notification(Recipient(), "BAD")))
    assert service.sent() == (result,)
    assert TaggedSender(TaggedSender(PushSender(), "A:"), "B:").send(item).text == "B:A:OK"
    code("INVALID_CONFIG", lambda: TaggedSender(PushSender(), 123))

def test_progression_tagged_sender_uses_inner_once_and_preserves_receipt():
    from app.domain.senders import NotificationSender
    calls = []
    original = DeliveryReceipt("PUSH", "device", "ORIGINAL")
    class Source(NotificationSender):
        def send(self, item): calls.append(item); return original
    item = Notification(Recipient(push_token="device"), "INPUT")
    result = TaggedSender(Source(), "TAG:").send(item)
    assert calls == [item] and result.text == "TAG:ORIGINAL"
    assert original.text == "ORIGINAL" and item.message == "INPUT"

from app.domain.senders import SuffixSender, EmailSender
from app.domain.notification import Notification
from app.support.types import Recipient

def test_progression_extra_lab06():
    original = Notification(Recipient(email="a@test"), "OK")
    sender = SuffixSender(EmailSender(), "!")
    receipt = sender.send(original)
    assert receipt.text == "OK!" and receipt.channel == "EMAIL"
    assert original.message == "OK"
    code("INVALID_CONFIG", lambda: SuffixSender(object(), "!"))
