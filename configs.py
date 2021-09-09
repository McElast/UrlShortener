"""Файл с различными настройками проекта"""
import string

# Адрес нашего домена для применения в качеставе базы для поля short_url модели ShortenUrl
# и любом другом месте по требованию
DOMAIN_URL = 'http://127.0.0.1:8000/'

# Время жизни сессий пользователей, записей в БД и кеше в рамках проекта (секунд)
OBJ_LIFETIME = 10 * 60

# Разрешенные символы для укороченной ссылки (чтобы пользователь не ввел недопустимые)
ALLOWED_SYMBOLS_FOR_LINK = string.ascii_letters + string.digits + '-'
