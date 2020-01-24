import random
import sys

from django.db.models import Avg
from django.http import JsonResponse

from gameplan.models import Game
from gatherer.models import Log
from recommender.models import RecommendationPairing
from recommender_libraries import title_similarity, title_popularity


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
    uid = request.user.id
    games_return_data = None
    if uid is not None:
        events = Log.objects.filter(user_id=uid).order_by('-created').values_list('content_id', flat=True).distinct()
        newest_events = list(events[:20])

        pairings = RecommendationPairing.objects.filter(from_game_id__in=newest_events)\
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
    uid = request.user.id
    games_return_data = None
    if uid is not None:
        events = Log.objects.filter(user_id=uid, event_type='detail_view_event').order_by('-created').values_list('content_id', flat=True).distinct()
        newest_events = list(events[:1])

        games = get_content_based_recommendations(request, newest_events[0], n)

        based_on_title = Game.objects.get(game_id=newest_events[0]).title
        games_return_data = {
            'user_id': uid,
            'based_on_title': based_on_title,
            'data': games
        }

    return JsonResponse(games_return_data, safe=False)
