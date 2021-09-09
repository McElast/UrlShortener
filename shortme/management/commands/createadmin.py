from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from urlizer.settings import ADMIN_NAME, ADMIN_PASS, ADMIN_MAIL


class Command(BaseCommand):
    """
    Создаем админа сайда для доступа к админ панели
    В docker-compose прописываем команду >>> python manage.py createadmin <<<
    """
    def handle(self, *args, **options):
        username = ADMIN_NAME
        if not User.objects.filter(username=username).exists():
            email = ADMIN_PASS
            password = ADMIN_MAIL
            print(f'Создается админ.аккаунт - {username} - {email}')
            User.objects.create_superuser(email=email, username=username, password=password)
        else:
            print('Админ уже есть!')
