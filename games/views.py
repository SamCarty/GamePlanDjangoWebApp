import sys

from django.http import JsonResponse
from django.shortcuts import render

from gameplan.models import Game, Screenshot


def index(request, game_id):
    return render(request, 'games/details.html')


def get_game_details(request, game_id):
    details = list(Game.objects.filter(game_id=game_id).values())
    details[0]['screenshots'] = get_screenshots_for_game(request, game_id)

    return JsonResponse(details, safe=False)


def get_screenshots_for_game(request, game_id):
    screenshot_ids = list(Game.screenshots.through.objects.filter(game_id=game_id).values())

    ids = list()
    for item in screenshot_ids:
        ids.append(str(item['screenshot_id']))

    urls = list(Screenshot.objects.filter(screenshot_id__in=ids).values())

    return urls
