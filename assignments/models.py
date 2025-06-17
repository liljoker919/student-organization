from django.db import models
from django.conf import settings
from django.utils import timezone
from classes.models import StudentClass


class Task(models.Model):
    TASK_TYPE_CHOICES = [
        ("assignment","Assignment"),
        ("test","Test")
    ]

    PRIORITY_CHOICES = [
        ("high","High"),
        ("medium","Medium"),
        ("low","Low")
    ]

    STATUS_CHOICES = [
        ("todo","To Do"),
        ("in_progress","In Progress"),
        ("complete","Complete")
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    task_type = models.CharField(max_length=20, choices=TASK_TYPE_CHOICES, default='assignment')
    name = models.CharField(max_length=250)
    student_class = models.ForeignKey(StudentClass, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    due_date = models.DateField()
    priority = models.CharField(max_length=15, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='todo')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # model property/method
    @property
    def is_late(self):
        return self.due_date < timezone.localdate() and self.status != 'complete'

    def __str__(self):
        return self.name




# Notification Model
class Notification(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.message[0:50]
