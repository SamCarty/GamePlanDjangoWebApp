import sys

from django.http import JsonResponse
from recommender_libraries import recommend
import logging

logger = logging.getLogger(__name__)


def get_content_based_recommendations(request, title, n=10):
    print(title, file=sys.stderr)
    titles = recommend.generate_recommendations(title, n)
    return JsonResponse(titles, safe=False)

