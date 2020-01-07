from django.db import models


class Genre(models.Model):
    genre_id = models.CharField(max_length=16, unique=True, primary_key=True)
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Game(models.Model):
    game_id = models.CharField(max_length=16, unique=True, primary_key=True)
    title = models.CharField(max_length=128)
    summary = models.CharField(max_length=1024)
    storyline = models.CharField(max_length=1024, null=True)
    genres = models.ManyToManyField(Genre, related_name='games', db_table='game_genre')
    ordered_keywords = models.CharField(max_length=2056, null=True)

    def __str__(self):
        return self.title
