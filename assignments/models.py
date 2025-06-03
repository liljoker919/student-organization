from django.db import models
from django.conf import settings
from classes.models import StudentClass
from datetime import date

# Task Model
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

    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    task_type = models.CharField(max_length=15,choices=TASK_TYPE_CHOICES,default='assignment')
    student_class = models.ForeignKey(StudentClass,on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    due_date = models.DateField()
    priority = models.CharField(max_length=15,choices=PRIORITY_CHOICES,default='medium')
    status = models.CharField(max_length=15,choices=STATUS_CHOICES,default='todo')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    # human-readable string representation
    def __str__(self):
        return self.name

    # model method/property
    @property
    def is_late(self):
        return self.due_date < date.today() and self.status != "complete"