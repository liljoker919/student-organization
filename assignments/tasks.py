from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import Task, Notification

@shared_task
def send_task_reminders():
    now = timezone.now().date()
    tomorrow = now + timedelta(days=1)

    due_soon_tasks = Task.objects.filter(
        due_date=tomorrow,
        status__in=["todo", "in_progress"]
    )

    for task in due_soon_tasks:
        # Check if a reminder already exists
        if not Notification.objects.filter(task=task, message__icontains="due tomorrow").exists():
            Notification.objects.create(
                user=task.user,
                task=task,
                message=f"Reminder: Your task '{task.name}' is due tomorrow ({task.due_date}).",
            )
