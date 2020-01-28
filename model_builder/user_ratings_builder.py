import os
import sys
from datetime import datetime

import django
from collections import defaultdict

import pytz
from django.db.models import Count

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gameplan_project.settings")
django.setup()
from django.contrib.auth.models import User
from gatherer.models import Log, UserRating
from gameplan.models import Game

weighting_buy = 100
weighting_wishlist = 75
weighting_details = 50
weighting_rec = 25


def get_log_data_for_user(user_id):
    data = Log.objects.filter(user_id=user_id).values().annotate(count=Count('created'))
    return data


def calculate_ratings_for_user(user_id):
    """ Calculates the 'rating' for a given user id based on the events that user triggered regarding each piece of
     content. This uses various weightings for each event and normalizes the results in a 1-10 scale. """

    # Acquire the raw log data.
    data = get_log_data_for_user(user_id)

    # Obtain the number of occurrences per event type.
    event_occurrences = dict()
    max_rating = 0
    for row in data:
        id = str(row['content_id'])
        if id not in event_occurrences.keys():
            event_occurrences[id] = defaultdict(int)

        event_occurrences[id][row['event_type']] = row['count']

    # Creates ratings using the weightings.
    ratings = dict()
    for key, item in event_occurrences.items():
        rating = weighting_buy * item['purchase_event'] + weighting_wishlist * item['wishlist_event'] +\
                 weighting_details * item['detail_view_event'] + weighting_rec * item['rec_view_event']

        max_rating = max(max_rating, rating)
        ratings[key] = rating

    # Normalize the data between 0-10.
    for id in ratings.keys():
        ratings[id] = 10 * ratings[id] / max_rating

    return ratings


def save_ratings(user_ratings, user_id):
    print(user_ratings, sys.stderr)
    for game_id, user_rating in user_ratings.items():
        if user_rating > 0:
            user = User.objects.get(id=user_id)
            game = Game.objects.get(game_id=game_id)
            UserRating(created=datetime.now(pytz.utc), user=user, game=game, user_rating=user_rating).save()


def calculate_ratings():
    users = Log.objects.values('user_id').distinct()
    print(users, sys.stderr)
    for user in users:
        print("New user " + str(user['user_id']), sys.stderr)
        if user['user_id'] is not None:
            id = user['user_id']
            user_ratings = calculate_ratings_for_user(id)

            save_ratings(user_ratings, id)


if __name__ == '__main__':
    print('Calculating ratings...')
    calculate_ratings()
