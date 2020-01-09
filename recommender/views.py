from django.http import JsonResponse
from recommender_libraries import recommend


def get_content_based_recommendations(request, game_id, n=10):
    games = recommend.generate_recommendations(game_id, n)

    games_return_data = {
        'source_id': game_id,
        'data': games
    }

    return JsonResponse(games_return_data, safe=False)

