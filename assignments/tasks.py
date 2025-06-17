from datetime import datetime, timedelta
from celery import shared_task
from .models import Task, Notification

@shared_task
def create_reminders():
    """Create notifications for tasks due in < 24 hours."""
    now = datetime.utcnow()
    deadline = now + timedelta(hours=24)

    tasks = Task.objects.filter(due_date__lte=deadline)
    for task in tasks:
        message = f"Your task '{task.name}' is due within 24 hours!"
        # To avoid duplicates, you might want to check first:
        if not Notification.objects.filter(user=task.user, message=message).exists():
            Notification.objects.create(user=task.user, message=message)
