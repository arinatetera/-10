import pytest
from decimal import Decimal
from datetime import date, datetime, timezone, timedelta
from app import api
from app.support.errors import DomainError


def assert_code(code, action):
    with pytest.raises(DomainError) as caught:
        action()
    assert caught.value.code == code

@pytest.mark.parametrize("destination,text",[("","OK"),("x",""),(" ","OK"),("x"," ")])
def test_review_invalid_receipt_content_is_not_stored(destination,text):
    from app.domain.notification import Notification
    from app.domain.senders import NotificationSender
    from app.services.notification_service import NotificationService
    from app.support.types import Recipient,DeliveryReceipt,Outbox
    class Wrong(NotificationSender):
        def send(self,notification):return DeliveryReceipt("EMAIL",destination,text)
    service=NotificationService({"EMAIL":Wrong()},Outbox())
    item=Notification(Recipient(email="a@example.test"),"OK")
    assert_code("INVALID_DELIVERY",lambda:service.send("EMAIL",item))
    assert service.sent() == ()
