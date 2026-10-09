import pytest
from app import api
from app.support.errors import DomainError


def assert_code(code, operation):
    with pytest.raises(DomainError) as error:
        operation()
    assert error.value.code == code

from app.support.types import Recipient, DeliveryReceipt

def test_additional_message_length_boundary():
    from app.domain.notification import Notification
    assert len(Notification(Recipient(), "x" * 1000).message) == 1000
    assert_code("MESSAGE_TOO_LONG", lambda: Notification(Recipient(), "x" * 1001))
