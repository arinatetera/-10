import pytest
from app import api
from app.support.errors import DomainError


def assert_code(code, operation):
    with pytest.raises(DomainError) as error:
        operation()
    assert error.value.code == code

from app.support.types import Recipient, DeliveryReceipt


def recipient():
    return Recipient(email="alice@example.test", phone="+000001", push_token="device-1")


@pytest.mark.parametrize("channel,destination", [
    ("EMAIL", "alice@example.test"), ("SMS", "+000001"),
])
def test_existing_channels(channel, destination):
    service = api.create()
    result = api.send(service, channel, recipient(), "Покупка 4.50 EUR")
    assert result == DeliveryReceipt(channel, destination, "Покупка 4.50 EUR")
    assert api.sent(service) == (result,)


def test_two_messages_keep_their_own_text():
    service = api.create()
    first = api.send(service, "EMAIL", recipient(), "Первое")
    second = api.send(service, "SMS", recipient(), "Второе")
    assert first.text == "Первое"
    assert second.text == "Второе"
    assert api.sent(service) == (first, second)


def test_repeat_is_two_explicit_deliveries():
    service = api.create()
    api.send(service, "EMAIL", recipient(), "Повтор")
    api.send(service, "EMAIL", recipient(), "Повтор")
    assert len(api.sent(service)) == 2


def test_unknown_channel_does_not_append():
    service = api.create()
    before = api.sent(service)
    assert_code("UNSUPPORTED_CHANNEL", lambda: api.send(service, "UNKNOWN", recipient(), "OK"))
    assert api.sent(service) == before


def test_delivery_is_returned_not_printed(capsys):
    receipt = api.send(api.create(), "SMS", recipient(), "OK")
    assert isinstance(receipt, DeliveryReceipt)
    assert capsys.readouterr().out == ""


def test_snapshot_and_receipt_are_read_only():
    service = api.create()
    receipt = api.send(service, "EMAIL", recipient(), "OK")
    snapshot = api.sent(service)
    with pytest.raises((AttributeError, TypeError)):
        receipt.text = "Изменено"
    api.send(service, "EMAIL", recipient(), "Позже")
    assert snapshot == (receipt,)
    assert len(api.sent(service)) == 2

@pytest.mark.parametrize("message", ["", "   ", "\t\n"])
def test_blank_message_is_rejected_without_delivery(message):
    service = api.create()
    before = api.sent(service)
    assert_code("INVALID_MESSAGE", lambda: api.send(service, "EMAIL", recipient(), message))
    assert api.sent(service) == before


def test_text_is_trimmed():
    assert api.send(api.create(), "SMS", recipient(), " OK ").text == "OK"


@pytest.mark.parametrize("channel,person", [
    ("EMAIL", Recipient(phone="+000001")),
    ("SMS", Recipient(email="alice@example.test")),
    ("EMAIL", Recipient(email="  ")),
])
def test_missing_channel_contact_does_not_append(channel, person):
    service = api.create()
    before = api.sent(service)
    assert_code("MISSING_CONTACT", lambda: api.send(service, channel, person, "OK"))
    assert api.sent(service) == before


def test_phone_only_recipient_can_receive_sms():
    receipt = api.send(api.create(), "SMS", Recipient(phone=" +000001 "), "OK")
    assert receipt.destination == "+000001"


def test_notification_itself_protects_message():
    from app.domain.notification import Notification
    assert_code("INVALID_MESSAGE", lambda: Notification(recipient(), " "))
    notification = Notification(recipient(), " OK ")
    assert notification.message == "OK"
    with pytest.raises(AttributeError):
        notification.message = ""

def test_abstract_sender_cannot_be_instantiated():
    from app.domain.senders import NotificationSender
    with pytest.raises(TypeError):
        NotificationSender()


@pytest.mark.parametrize("name,channel,destination", [
    ("EmailSender", "EMAIL", "alice@example.test"),
    ("SmsSender", "SMS", "+000001"),
])
def test_senders_share_one_contract(name, channel, destination):
    from app.domain import senders
    from app.domain.notification import Notification
    sender = getattr(senders, name)()
    assert isinstance(sender, senders.NotificationSender)
    assert sender.send(Notification(recipient(), "OK")) == DeliveryReceipt(channel, destination, "OK")


@pytest.mark.parametrize("name", ["EmailSender", "SmsSender"])
def test_sender_alone_checks_its_contact(name):
    from app.domain import senders
    from app.domain.notification import Notification
    assert_code("MISSING_CONTACT", lambda: getattr(senders, name)().send(Notification(Recipient(), "OK")))


def test_sender_is_used_in_the_real_path(monkeypatch):
    from app.domain.senders import EmailSender
    calls = []
    def send(self, notification):
        calls.append(notification)
        return DeliveryReceipt("EMAIL", "alice@example.test", "CONTROL")
    monkeypatch.setattr(EmailSender, "send", send)
    receipt = api.send(api.create(), "EMAIL", recipient(), "OK")
    assert receipt.text == "CONTROL"
    assert len(calls) == 1

def make_injected(sender, channel="EMAIL"):
    from app.services.notification_service import NotificationService
    from app.support.types import Outbox
    return NotificationService({channel: sender}, Outbox())


def test_supplied_sender_is_called_once():
    from app.domain.senders import NotificationSender
    from app.domain.notification import Notification
    class ControlSender(NotificationSender):
        def __init__(self):
            self.calls = 0
        def send(self, notification):
            self.calls += 1
            return DeliveryReceipt("EMAIL", "control@example.test", "CONTROL")
    sender = ControlSender()
    service = make_injected(sender)
    result = service.send("EMAIL", Notification(recipient(), "OK"))
    assert result.text == "CONTROL"
    assert sender.calls == 1
    assert service.sent() == (result,)


def test_mapping_is_copied_but_sender_is_not():
    from app.domain.senders import EmailSender, SmsSender
    from app.domain.notification import Notification
    from app.services.notification_service import NotificationService
    from app.support.types import Outbox
    senders = {"EMAIL": EmailSender()}
    service = NotificationService(senders, Outbox())
    senders.clear()
    result = service.send("EMAIL", Notification(recipient(), "OK"))
    assert result.channel == "EMAIL"
    # SMS was never registered in this particular configuration.
    assert_code("UNSUPPORTED_CHANNEL", lambda: service.send("SMS", Notification(recipient(), "OK")))


def test_empty_mapping_is_not_replaced_by_defaults():
    from app.services.notification_service import NotificationService
    from app.domain.notification import Notification
    from app.support.types import Outbox
    service = NotificationService({}, Outbox())
    assert_code("UNSUPPORTED_CHANNEL", lambda: service.send("EMAIL", Notification(recipient(), "OK")))
    assert service.sent() == ()


def test_builds_have_independent_outboxes():
    first, second = api.create(), api.create()
    api.send(first, "EMAIL", recipient(), "Первое")
    assert len(api.sent(first)) == 1
    assert api.sent(second) == ()


def test_dependency_error_is_not_success():
    from app.domain.senders import NotificationSender
    from app.domain.notification import Notification
    class Broken(NotificationSender):
        def send(self, notification):
            raise DomainError("DELIVERY_FAILED")
    service = make_injected(Broken())
    assert_code("DELIVERY_FAILED", lambda: service.send("EMAIL", Notification(recipient(), "OK")))
    assert service.sent() == ()


@pytest.mark.parametrize("value", [None, DeliveryReceipt("SMS", "+000001", "OK")])
def test_invalid_receipt_is_not_stored(value):
    from app.domain.senders import NotificationSender
    from app.domain.notification import Notification
    class Invalid(NotificationSender):
        def send(self, notification):
            return value
    service = make_injected(Invalid())
    assert_code("INVALID_DELIVERY", lambda: service.send("EMAIL", Notification(recipient(), "OK")))
    assert service.sent() == ()


def test_intentionally_shared_outbox_stays_shared():
    from app.domain.senders import EmailSender
    from app.domain.notification import Notification
    from app.services.notification_service import NotificationService
    from app.support.types import Outbox
    outbox = Outbox()
    first = NotificationService({"EMAIL": EmailSender()}, outbox)
    second = NotificationService({"EMAIL": EmailSender()}, outbox)
    first.send("EMAIL", Notification(recipient(), "OK"))
    assert len(second.sent()) == 1

def test_push_is_registered_and_records_once():
    service = api.create()
    result = api.send(service, "PUSH", recipient(), "Покупка")
    assert result == DeliveryReceipt("PUSH", "device-1", "Покупка")
    assert api.sent(service) == (result,)


def test_push_sender_obeys_the_same_contract():
    from app.domain.notification import Notification
    from app.domain.senders import PushSender, NotificationSender
    sender = PushSender()
    assert isinstance(sender, NotificationSender)
    assert sender.send(Notification(recipient(), "OK")) == DeliveryReceipt("PUSH", "device-1", "OK")


@pytest.mark.parametrize("token", [None, " "])
def test_push_without_token_does_not_append(token):
    service = api.create()
    assert_code("MISSING_CONTACT", lambda: api.send(service, "PUSH", Recipient(push_token=token), "OK"))
    assert api.sent(service) == ()
