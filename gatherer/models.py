from django.contrib.auth.models import User
from django.db import models

from gameplan.models import Game


class Log(models.Model):
    created = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    event_type = models.CharField(max_length=32)
    content_id = models.CharField(max_length=32)
    session_id = models.CharField(max_length=64)


class UserRating(models.Model):
    created = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, null=True)
    user_rating = models.FloatField()
