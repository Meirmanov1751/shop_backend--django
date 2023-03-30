from rest_framework import serializers


def validate_phone(phone):
    import re
    phone_valid = re.compile(r'^\+?(7)?\d{11,13}$')
    if phone_valid.search(phone) is not None:
        if phone[0] == '8':
            phone = phone[1:]
        if phone[:2] == '+7':
            phone = phone[2:]
    else:
        raise serializers.ValidationError('Ошибка в номере')
    return phone