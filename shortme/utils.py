import random
from django.core.exceptions import ValidationError
import configs


def shorten():
    """
    Генерирует сокращенный  вариант ссылки
    (уникальный в рамках модели ShortenUrl)
    """
    short_url = ''.join(random.choices(configs.ALLOWED_SYMBOLS_FOR_LINK, k=10))
    return short_url


def suitable_symbols_validator(user_short_url):
    """
    Проверяем, ввел ли пользователь только разрешенные символы
    при выборе собственного адреса для сокращенной ссылки
    """
    for letter in user_short_url:
        if letter not in configs.ALLOWED_SYMBOLS_FOR_LINK:
            raise ValidationError(f'<< {letter} >> не подходит для адреса ссылки. '
                                  f'Используйте только латиницу, числа и символ дефиса')
