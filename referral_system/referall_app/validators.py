import re

from django.core.exceptions import ValidationError

PHONE_NUMBER_PATTERN = r'^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$'
WRONG_PHONE_NUMBER_FORMAT_MESSAGE = 'Некорректный формат номера телефона'


def validate_phone_number(phone_number):
    """Валидируем номер телефона по шаблону"""
    if re.match(PHONE_NUMBER_PATTERN, phone_number) is None:
        raise ValidationError(WRONG_PHONE_NUMBER_FORMAT_MESSAGE)
    return phone_number
