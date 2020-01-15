from django.http import JsonResponse
from gameplan.models import Game
from recommender_libraries import recommend


def get_content_based_recommendations(request, game_id, n=10):
    games = recommend.generate_recommendations(game_id, n)

    game_data = list()
    for g_id in games:
        game_data.append(list(Game.objects.filter(game_id=g_id).values())[0])

    games_return_data = {
        'source_id': game_id,
        'data': game_data
    }

    return JsonResponse(games_return_data, safe=False)
