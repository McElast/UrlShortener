import datetime

from celery import shared_task
from celery.utils.log import get_task_logger

import configs
from .models import ShortenUrl

logger = get_task_logger(__name__)


@shared_task(name='clear_mysql')
def clear_mysql_task():
    """
    Задача очистки базы данных от устаревший значений.
    Запускается по расписанию - словарь CELERY_BEAT_SCHEDULE в файле settings.py
    """
    logger.info('Проводим чистку')
    delete_time = datetime.datetime.now() - datetime.timedelta(seconds=configs.OBJ_LIFETIME)
    ShortenUrl.objects.filter(added__lt=delete_time).delete()
