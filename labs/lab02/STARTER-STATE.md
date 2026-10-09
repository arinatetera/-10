# Проверка исходного кода

Успешных обязательных проверок: **7**. С ошибками: **9**.

Эти ошибки связаны с заданием. После выполнения обязательной части все проверки должны пройти.

## Проверки, которые пока не проходят

- `tests.test_contract::test_blank_message_is_rejected_without_delivery[   ]`
- `tests.test_contract::test_blank_message_is_rejected_without_delivery[\t\n]`
- `tests.test_contract::test_blank_message_is_rejected_without_delivery[]`
- `tests.test_contract::test_missing_channel_contact_does_not_append[EMAIL-person0]`
- `tests.test_contract::test_missing_channel_contact_does_not_append[EMAIL-person2]`
- `tests.test_contract::test_missing_channel_contact_does_not_append[SMS-person1]`
- `tests.test_contract::test_notification_itself_protects_message`
- `tests.test_contract::test_phone_only_recipient_can_receive_sms`
- `tests.test_contract::test_text_is_trimmed`

Если список отличается или тесты не запускаются из-за ошибки установки или импорта, сообщите преподавателю. Не отключайте проверки.
