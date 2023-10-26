import os
from celery import Celery
from celery.schedules import crontab

# Установка переменной окружения DJANGO_SETTINGS_MODULE
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MMORPG.settings')

# Создание объекта Celery
app = Celery('MMORPG')

# Конфигурация Celery из настроек Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Установка временной зоны
app.conf.timezone = 'Europe/Moscow'

# Поиск и автоматическое обнаружение задач
app.autodiscover_tasks()

# Задачи и расписание
app.conf.beat_schedule = {
    'send_weekly_email': {
        'task': 'board.tasks.send_weekly_email',
        'schedule': crontab(hour=11, minute=0, day_of_week='sunday'),
    },
}


