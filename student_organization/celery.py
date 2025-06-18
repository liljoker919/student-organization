from celery import Celery
from celery.schedules import crontab
import os
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_organization.settings')

app = Celery('student_organization')

app.conf.update(
    broker_url = settings.CELERY_BROKER_URL,
    result_backend = settings.CELERY_RESULT_BACKEND,
    timezone = settings.CELERY_TIMEZONE,
    enable_utc = getattr(settings, 'CELERY_ENABLE_UTC', True),
)

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send_reminder_every_hour': {
        'task': 'assignments.tasks.send_task_reminders',
        'schedule': crontab(minute='0'),  # executes at the start of every hour
    },
}