import pytest
from app import api
from app.support.errors import DomainError


def assert_code(code, operation):
    with pytest.raises(DomainError) as error:
        operation()
    assert error.value.code == code

from app.support.types import Recipient, DeliveryReceipt

def test_filter_does_not_resend_or_change_outbox():
    service = api.create()
    email = api.send(service, "EMAIL", Recipient(email="a@example.test"), "OK")
    api.send(service, "PUSH", Recipient(push_token="device"), "OK")
    before = api.sent(service)
    assert service.sent_for_channel("EMAIL") == (email,)
    assert service.sent_for_channel("SMS") == ()
    assert api.sent(service) == before
