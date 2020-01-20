from django.contrib.auth.models import User
from django.db import models


class Log(models.Model):
    created = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event_type = models.CharField(max_length=32)
    content_id = models.CharField(max_length=32)
    session_id = models.CharField(max_length=64)
