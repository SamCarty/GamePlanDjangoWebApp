from django.http import JsonResponse
from gameplan.models import Game
from recommender_libraries import title_similarity, title_popularity


def get_content_based_recommendations(request, game_id, n=10):
    """ Gets the n most similar titles to the given game_id
     @:returns a JSON response containing information about each similar game."""
    games = title_similarity.generate_recommendations(game_id, n)

    game_data = list()
    for g_id in games:
        game_data.append(list(Game.objects.filter(game_id=g_id).values())[0])

    games_return_data = {
        'source_id': game_id,
        'data': game_data
    }

    return JsonResponse(games_return_data, safe=False)


def get_top_charts_recommendations(request, n=10):
    """ Gets the n most popular titles currently.
     @:returns a queryset of titles. """
    return title_popularity.generate_recommendations(n)

