from django.core.validators import MinLengthValidator
from django.db import models

from .utils import shorten, suitable_symbols_validator


class ShortenUrl(models.Model):
    """
    Модель для сохранения в БД сокращенной ссылки.
    Поля:
    - original_url - принимает исходный интернет-адрес пользователя
    - short_url - показывает преобразованный URL
    - added - дата добавления записи в БД
    - client_session - идентификатор сессии 'session_key' из request и таблицы Session
    """
    original_url = models.URLField(max_length=1000, verbose_name='Исходный адрес')
    short_url_part = models.CharField(max_length=20, unique=True, verbose_name='Короткий адрес без домена',
                                      null=True, blank=True, db_index=True,
                                      validators=[MinLengthValidator(2), suitable_symbols_validator],
                                      error_messages={'unique': 'Такой адрес уже есть в базе. Выберите другой',
                                                      'max_length': 'Превышена длина ссылки в 20 символов!'})
    added = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    client_session = models.CharField(max_length=1200, verbose_name='Идентификатор пользователя')

    def __str__(self):
        return f'{self.original_url}'

    def save(self, *args, **kwargs):
        if not self.short_url_part:
            self.short_url_part = shorten()
        return super().save(*args, **kwargs)
