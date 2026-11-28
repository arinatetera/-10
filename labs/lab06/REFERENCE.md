# Notification: справка для ЛР6

Сообщение содержит получателя и текст. Отправитель формирует квитанцию, сервис сохраняет успешную квитанцию в журнал. Реальной доставки по сети нет.

Здесь перечислены типы текущей работы. Что требуется реализовать и какие файлы можно менять, указано в [TASK.md](TASK.md).

## Предметные объекты и исполнители

| Тип и конструктор | Публичные действия и свойства | Файл |
|---|---|---|
| `Notification(recipient: Recipient, message: str)` | `recipient`, `message` | `app/domain/notification.py` |
| `NotificationSender()` | `send(notification: Notification)` | `app/domain/senders.py` |
| `EmailSender()` | `send(notification: Notification)` | `app/domain/senders.py` |
| `SmsSender()` | `send(notification: Notification)` | `app/domain/senders.py` |
| `PushSender()` | `send(notification: Notification)` | `app/domain/senders.py` |
| `TaggedSender(sender, prefix)` | `send(notification)` | `app/domain/senders.py` |
| `SuffixSender(sender, suffix)` | `send(notification)` | `app/domain/senders.py` |

Свойства читаются без скобок. Поля объекта-значения не меняются присваиванием; результат операции создаётся отдельно. Для наследника без собственного конструктора показаны аргументы конструктора базового класса.

## Вызов сервиса

| Метод | Сигнатура |
|---|---|
| `__init__` | `NotificationService(senders: Mapping[str, NotificationSender], outbox: Outbox)` |
| `send` | `send(channel: str, notification: Notification)` |
| `sent` | `sent()` |

`app/api.py` — готовая внешняя граница; не изменяйте её. Вызов попадает в сервис из указанного модуля. Подробные примеры создания входных объектов находятся в открытых тестах текущей папки.

В `app/services/assembly.py` находятся стандартные конфигурации. Переданный объект сохраняется, а отсутствие обозначается `None`. Пустой список или словарь не равен отсутствию настройки. Копия контейнера не означает копирования исполнителей.

Сигнатура сборки: `build_service()`.

## Готовые результаты и ошибки

`DomainError` находится в `app/support/errors.py`; код доступен через `error.code`. В разрешённых методах используйте готовые проверки, а не новую иерархию исключений.

`Recipient(email=None, phone=None, push_token=None)`, `DeliveryReceipt(channel, destination, text)` и `Outbox` находятся в `app/support/types.py`. `contact()` проверяет непустой контакт и возвращает строку без пробелов по краям. `validate_receipt()` отклоняет неподходящую квитанцию с `INVALID_DELIVERY`. Отправитель возвращает результат; только сервис записывает его в журнал.

## Проверка поведения

`tests/test_contract.py` и `tests/test_review_contract.py` проверяют предметные правила. `tests/test_progression.py` проверяет последовательности обращений и настройки текущей работы. Ни один результат теста не является командой менять защищённый API или тесты.

Ожидаемый стартовый результат — в [STARTER-STATE.md](STARTER-STATE.md). Проверка из корня проекта: `python check.py lab06`.
