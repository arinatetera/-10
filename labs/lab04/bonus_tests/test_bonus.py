import pytest
from app import api
from app.support.errors import DomainError


def assert_code(code, operation):
    with pytest.raises(DomainError) as error:
        operation()
    assert error.value.code == code

from app.support.types import Recipient, DeliveryReceipt

def test_diagnostic_delegates_to_description():
    from app.domain.notification import Notification
    from app.services.notification_service import diagnostic
    class ControlNotification(Notification):
        def describe(self):
            return "CONTROL"
    assert diagnostic(ControlNotification(Recipient(), "OK")) == "CONTROL"
