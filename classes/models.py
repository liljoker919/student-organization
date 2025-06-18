from django.db import models
from django.conf import settings


class StudentClass(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    color = models.CharField(max_length=50)
    icon = models.URLField(max_length=500)
    teacher = models.CharField(max_length=250)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()


    def __str__(self):
        return self.name