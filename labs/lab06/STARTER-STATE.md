# Исходные проверки ЛР6

Успешных проверок: **38**. Ожидаемых падений: **7**.

Не завершены новое поведение, его сочетание с прежними правилами и подключение. Отдельные проверки сравнивают настройки одного класса и поведение после отказа.

Падения ниже связаны с конкретными требованиями [TASK.md](TASK.md). После обязательной части все они должны пройти. Бонус проверяется отдельно и не входит в эти числа.

## Новые последовательности и конфигурации

- `tests.test_progression::test_progression_extra_lab06`
- `tests.test_progression::test_progression_tagged_sender_preserves_message_and_journal`
- `tests.test_progression::test_progression_tagged_sender_uses_inner_once_and_preserves_receipt`

## Предметный контракт и общий интерфейс

- `tests.test_contract::test_push_is_registered_and_records_once`
- `tests.test_contract::test_push_sender_obeys_the_same_contract`
- `tests.test_contract::test_push_without_token_does_not_append[ ]`
- `tests.test_contract::test_push_without_token_does_not_append[None]`

## Порядок проверки

Из корня проекта: `python check.py lab06`. Сначала прочитайте первый traceback и ожидаемый результат сценария. Не отключайте тесты, которые пока не проходят.

Ошибка импорта или установки не относится к заданию. Если исходный набор результатов отличается, сохраните вывод и сообщите преподавателю; не удаляйте решения и служебные файлы.
