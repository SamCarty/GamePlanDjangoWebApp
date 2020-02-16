import sys
import random

from django.db.models import Avg
from django.http import JsonResponse

from gameplan.models import Game, Genre
from gatherer.models import Log, UserRating
from recommender.models import RecommendationPairing
from recommender_libraries import title_similarity, title_popularity
from model_builder.user_ratings_builder import calculate_ratings, get_rating_for_user


def get_content_based_recommendations_json(request, game_id, n=10):
    """ Gets the n most similar titles to the given game_id
     @:returns a JSON response containing information about each similar game."""
    games = get_content_based_recommendations(request, game_id, n)
    games_return_data = {
        'original_game_id': game_id,
        'data': games
    }

    return JsonResponse(games_return_data, safe=False)


def get_content_based_recommendations(request, game_id, n=10):
    """ Gets the n most similar titles to the given game_id
    @:returns a list containing information about each similar game."""
    games = title_similarity.generate_recommendations(game_id, n)

    game_data = list()
    for g_id in games:
        game_data.append(list(Game.objects.filter(game_id=g_id).values())[0])

    return game_data


def get_top_charts_recommendations(request, n=10):
    """ Gets the n most popular titles currently.
     @:returns a queryset of titles. """
    return title_popularity.generate_recommendations(n)


def get_bought_together_recommendations(request, game_id, n=10):
    """ Get the n most bought together titles based on the the given game.
     @:returns a JSON response containing information about each bought together game. """
    from_game = Game.objects.get(game_id=game_id)
    recs = RecommendationPairing.objects.filter(from_game=from_game).order_by('-confidence')[:n]

    game_data = list()
    for rec in recs:
        to_game = rec.to_game
        game_data.append(list(Game.objects.filter(game_id=to_game.game_id).values())[0])

    games_return_data = {
        'original_game_id': game_id,
        'data': game_data
    }

    print(games_return_data, sys.stderr)
    return JsonResponse(games_return_data, safe=False)


def get_users_like_you_recommendations(request, n=50):
    """ Get n number of games based on users similar to the logged-in user.
     @:returns a JSON response containing information about 'like you' game. """
    uid = request.user.id
    games_return_data = None
    if uid is not None:
        events = Log.objects.filter(user_id=uid).order_by('-created').values_list('content_id', flat=True).distinct()
        newest_events = list(events[:20])

        pairings = RecommendationPairing.objects.filter(from_game_id__in=newest_events) \
            .annotate(avg_confidence=Avg('confidence')).order_by('-avg_confidence')

        game_data = list()
        for rec in pairings:
            to_game = rec.to_game
            game = list(Game.objects.filter(game_id=to_game.game_id).values())[0]
            if game not in game_data:
                game_data.append(game)

        games_return_data = {
            'user_id': uid,
            'data': game_data[:n]
        }

    return JsonResponse(games_return_data, safe=False)


def get_similar_to_recent_recommendations(request, n=50):
    """ Get n number of games based on what the user has looked at recently
     @:returns a JSON response containing information about similar game.  """
    uid = request.user.id
    games_return_data = None
    if uid is not None:
        events = Log.objects.filter(user_id=uid, event_type='detail_view_event').order_by('-created') \
            .values_list('content_id', flat=True).distinct()
        newest_events = list(events[:1])

        games = get_content_based_recommendations(request, newest_events[0], n)

        based_on_title = Game.objects.get(game_id=newest_events[0]).title
        games_return_data = {
            'user_id': uid,
            'based_on_title': based_on_title,
            'data': games
        }

    return JsonResponse(games_return_data, safe=False)


def get_top_genre_recommendations(request, genre_id, n=50):
    uid = request.user.id
    games_return_data = None
    if uid is not None:
        games = list(Game.objects.select_related().filter(genres__genre_id=genre_id).order_by('-popularity')[:n]
                     .values())
        games_return_data = {
            'user_id': uid,
            'data': games
        }

    return JsonResponse(games_return_data, safe=False)


def get_recommender_categories(request):
    cats = list()
    if request.user.is_authenticated:
        game_ratings = get_rating_for_user(request.user)

        # Content-based
        content_recs = game_ratings.order_by('-user_rating').select_related() \
                           .values('game_id', 'game__title').distinct()[:5]
        for game in content_recs:
            if game not in cats:
                dic = dict()
                dic['content_based'] = game
                cats.append(dic)

        # Genres
        content_recs = game_ratings.order_by('-user_rating').select_related() \
                           .values('game__genres__genre_id', 'game__genres__name').distinct()[:5]
        for genre in content_recs:
            if genre not in cats:
                dic = dict()
                dic['genre_based'] = genre
                cats.append(dic)

        random.shuffle(cats)

    return cats


"""
    def get_recommender_categories(request):
    cats = dict()
    if request.user.is_authenticated:
        game_ratings = get_rating_for_user(request.user)

        # Content-based
        content_recs = game_ratings.order_by('-user_rating').select_related() \
            .values('game_id', 'game__title').distinct()[:5]
        content_recs_list = list()
        for game in content_recs:
            if game not in content_recs_list:
                content_recs_list.append(game)

        print(content_recs_list, sys.stderr)
        cats['content_based'] = content_recs_list

        # Genres
        content_recs = game_ratings.order_by('-user_rating').select_related() \
                           .values('game__genres__genre_id', 'game__genres__name').distinct()[:5]
        genres_list = list()
        for genre in content_recs:
            if genre not in genres_list:
                genres_list.append(genre)

        cats['genre_based'] = genres_list

    return cats
    """
