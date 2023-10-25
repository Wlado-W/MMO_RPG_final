import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MMORPG.settings')


app = Celery('MMORPG')


app.config_from_object('django.conf:settings', namespace='CELERY')


app.conf.timezone = 'Europe/Moscow'


app.autodiscover_tasks()


app.conf.beat_schedule = {
    'send_mail_sunday_11am': {
        'task': 'board.tasks.send_mail_sunday_11am',
        'schedule': crontab(hour=11, minute=0, day_of_week='sunday'),
    },
}

