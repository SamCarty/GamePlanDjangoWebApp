# Generated by Django 2.2.5 on 2020-01-06 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gameplan', '0002_game_storyline'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='ordered_keywords',
            field=models.CharField(max_length=2056, null=True),
        ),
    ]
