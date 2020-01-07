import sys

from django.http import JsonResponse
from recommender_libraries import recommend
import logging

logger = logging.getLogger(__name__)


def get_content_based_recommendations(request, title, n=10):
    print(title, file=sys.stderr)
    games = recommend.generate_recommendations(title, n)

    games_return_data = {
        'source_id': title,
        'data': games
    }

    return JsonResponse(games_return_data, safe=False)

