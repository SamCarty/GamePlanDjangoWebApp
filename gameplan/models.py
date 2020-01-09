from django.db import models


class Image(models.Model):
    image_id = models.CharField(max_length=16, unique=True, primary_key=True)
    url = models.URLField(max_length=200)

    def __str__(self):
        return self.url


class Genre(models.Model):
    genre_id = models.CharField(max_length=16, unique=True, primary_key=True)
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Cover(models.Model):
    cover_id = models.CharField(max_length=16, unique=True, primary_key=True)
    url = models.URLField(max_length=200)


class Franchise(models.Model):
    franchise_id = models.CharField(max_length=16, unique=True, primary_key=True)
    name = models.CharField(max_length=128)


class GameEngine(models.Model):
    game_engine_id = models.CharField(max_length=16, unique=True, primary_key=True)
    name = models.CharField(max_length=128)


class GameMode(models.Model):
    game_mode_id = models.CharField(max_length=16, unique=True, primary_key=True)
    name = models.CharField(max_length=128)


class Company(models.Model):
    company_id = models.CharField(max_length=16, unique=True, primary_key=True)
    name = models.CharField(max_length=128)


class InvolvedCompany(models.Model):
    involved_company_id = models.CharField(max_length=16, unique=True, primary_key=True)
    company = models.ForeignKey(Company, on_delete=None)
    developer = models.BooleanField()
    publisher = models.BooleanField()


class Platform(models.Model):
    platform_id = models.CharField(max_length=16, unique=True, primary_key=True)
    name = models.CharField(max_length=128)


class PlayerPerspective(models.Model):
    player_perspective_id = models.CharField(max_length=16, unique=True, primary_key=True)
    name = models.CharField(max_length=128)


class ReleaseDate(models.Model):
    release_date_id = models.CharField(max_length=16, unique=True, primary_key=True)
    date = models.CharField(max_length=12, null=True)
    human = models.CharField(max_length=12, null=True)
    platform = models.ForeignKey(Platform, on_delete=None)
    region = models.IntegerField(null=True)


class Screenshot(models.Model):
    screenshot_id = models.CharField(max_length=16, unique=True, primary_key=True)
    url = models.URLField(max_length=200)


class Theme(models.Model):
    theme_id = models.CharField(max_length=16, unique=True, primary_key=True)
    name = models.CharField(max_length=128)


class Video(models.Model):
    id = models.CharField(max_length=16, unique=True, primary_key=True)
    video_id = models.CharField(max_length=16)


class Website(models.Model):
    website_id = models.CharField(max_length=16, unique=True, primary_key=True)
    url = models.URLField(max_length=200)


class Game(models.Model):
    game_id = models.CharField(max_length=16, unique=True, primary_key=True)
    title = models.CharField(max_length=128)
    summary = models.CharField(max_length=1024)
    storyline = models.CharField(max_length=1024, null=True)
    genres = models.ManyToManyField(Genre, db_table='game_genre')
    ordered_keywords = models.CharField(max_length=2056, null=True)
    cover = models.URLField(max_length=200, null=True)

    category = models.CharField(max_length=3, null=True)
    first_release_date = models.CharField(max_length=12, null=True)
    franchise = models.ForeignKey(Franchise, on_delete=None, null=True)
    game_engines = models.ManyToManyField(GameEngine, db_table='game_game_engine')
    game_modes = models.ManyToManyField(GameMode, db_table='game_game_mode')
    hypes = models.IntegerField(null=True)
    involved_companies = models.ManyToManyField(InvolvedCompany, db_table='game_involved_company')
    keywords = models.CharField(max_length=5000, null=True)
    platforms = models.ManyToManyField(Platform, db_table='game_platform')
    player_perspectives = models.ManyToManyField(PlayerPerspective, db_table='game_player_perspectives')
    popularity = models.FloatField(null=True)
    release_dates = models.ManyToManyField(ReleaseDate, db_table='game_release_dates')
    screenshots = models.ManyToManyField(Screenshot, db_table='game_screenshots')
    themes = models.ManyToManyField(Theme, db_table='game_theme')
    total_rating = models.FloatField(null=True)
    total_rating_count = models.IntegerField(null=True)
    url = models.URLField(max_length=200, null=True)
    videos = models.ManyToManyField(Video, db_table='game_video')
    websites = models.ManyToManyField(Website, db_table='game_website')


    def __str__(self):
        return self.title
