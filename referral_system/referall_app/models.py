from django.contrib.auth.models import AbstractUser
from django.db import models

from .validators import validate_phone_number

MAX_PHONE_NUMBER_LENGTH = 16
MAX_CONFCODE_LENGTH = 4
MAX_INVITE_CODE_LENGTH = 6
MAX_USERNAME_LENGTH = 150
CHARACTERS_FOR_CONFCODE = '0123456789'
CHARACTERS_FOR_INVITECODE = (
    'ABCDEFGHJKLMNOPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz1234567890'
)


class ReferallUser(AbstractUser):
    """Кастомная модель пользователя"""
    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=150,
        help_text='Укажите имя пользователя',
        blank=True,
        null=True
    )
    phone_number = models.CharField(
        verbose_name='Номер телефона',
        max_length=MAX_PHONE_NUMBER_LENGTH,
        unique=True,
        help_text='Укажите номер телефона',
        validators=(validate_phone_number,)
    )
    confirmation_code = models.CharField(
        verbose_name='Код подтверждения',
        max_length=MAX_CONFCODE_LENGTH,
        blank=True,
        null=True,
        help_text='Введите код подтверждения',
    )
    invitation_code = models.CharField(
        verbose_name='Инвайт-код пользователя',
        max_length=MAX_INVITE_CODE_LENGTH
    )
    invited_by = models.CharField(
        verbose_name='Инвайт-код другого пользователя',
        max_length=MAX_INVITE_CODE_LENGTH
    )

    def __str__(self):
        return self.phone_number

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['username']
