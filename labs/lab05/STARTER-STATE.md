# Исходные проверки ЛР5

Успешных проверок: **11**. Ожидаемых падений: **28**.

Не завершены использование переданных зависимостей, сборка и основной путь операции. Проверки вызывают разные конфигурации и ошибающегося исполнителя; ошибка не должна превращаться в успешный результат или повторную операцию.

Падения ниже связаны с конкретными требованиями [TASK.md](TASK.md). После обязательной части все они должны пройти. Бонус проверяется отдельно и не входит в эти числа.

## Новые последовательности и конфигурации

- `tests.test_progression::test_progression_extra_lab05`
- `tests.test_progression::test_progression_failed_send_is_not_recorded`
- `tests.test_progression::test_progression_sender_error_has_no_phantom_receipt`

## Предметный контракт и общий интерфейс

- `tests.test_contract::test_builds_have_independent_outboxes`
- `tests.test_contract::test_delivery_is_returned_not_printed`
- `tests.test_contract::test_dependency_error_is_not_success`
- `tests.test_contract::test_empty_mapping_is_not_replaced_by_defaults`
- `tests.test_contract::test_existing_channels[EMAIL-alice@example.test]`
- `tests.test_contract::test_existing_channels[SMS-+000001]`
- `tests.test_contract::test_intentionally_shared_outbox_stays_shared`
- `tests.test_contract::test_invalid_receipt_is_not_stored[None]`
- `tests.test_contract::test_invalid_receipt_is_not_stored[value1]`
- `tests.test_contract::test_mapping_is_copied_but_sender_is_not`
- `tests.test_contract::test_missing_channel_contact_does_not_append[EMAIL-person0]`
- `tests.test_contract::test_missing_channel_contact_does_not_append[EMAIL-person2]`
- `tests.test_contract::test_missing_channel_contact_does_not_append[SMS-person1]`
- `tests.test_contract::test_phone_only_recipient_can_receive_sms`
- `tests.test_contract::test_repeat_is_two_explicit_deliveries`
- `tests.test_contract::test_sender_is_used_in_the_real_path`
- `tests.test_contract::test_snapshot_and_receipt_are_read_only`
- `tests.test_contract::test_supplied_sender_is_called_once`
- `tests.test_contract::test_text_is_trimmed`
- `tests.test_contract::test_two_messages_keep_their_own_text`
- `tests.test_contract::test_unknown_channel_does_not_append`
- `tests.test_review_contract::test_review_invalid_receipt_content_is_not_stored[ -OK]`
- `tests.test_review_contract::test_review_invalid_receipt_content_is_not_stored[-OK]`
- `tests.test_review_contract::test_review_invalid_receipt_content_is_not_stored[x- ]`
- `tests.test_review_contract::test_review_invalid_receipt_content_is_not_stored[x-]`

## Порядок проверки

Из корня проекта: `python check.py lab05`. Сначала прочитайте первый traceback и ожидаемый результат сценария. Не отключайте тесты, которые пока не проходят.

Ошибка импорта или установки не относится к заданию. Если исходный набор результатов отличается, сохраните вывод и сообщите преподавателю; не удаляйте решения и служебные файлы.
