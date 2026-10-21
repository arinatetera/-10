from app.services.notification_service import new_service
from app.domain.notification import Notification
from app.support.types import Recipient
from app.support.errors import DomainError

service = new_service()

# 1. Успешная отправка FIRST
first = service.send(
    "EMAIL",
    Notification(Recipient(email="first@example.com"), "FIRST"),
)
print("FIRST:", first)

# 2. Отправка без нужного контакта
try:
    service.send(
        "EMAIL",
        Notification(Recipient(email=None), "SECOND"),
    )
except DomainError as error:
    print("SECOND error:", error)

# 3. Успешная отправка THIRD
third = service.send(
    "EMAIL",
    Notification(Recipient(email="third@example.com"), "THIRD"),
)
print("THIRD:", third)

# 4. Проверяем журнал
messages = service.sent()
print("Outbox:", messages)

assert first.text == "FIRST"
assert third.text == "THIRD"
assert len(messages) == 2
assert messages[0].text == "FIRST"
assert messages[1].text == "THIRD"

print("ALL CHECKS PASSED")