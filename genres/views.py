import sys
from operator import attrgetter

from django.http import JsonResponse

from gameplan.models import Genre


def get_all_genres(request):
    genres = list(Genre.objects.values())
    return JsonResponse(genres, safe=False)
