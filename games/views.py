from django.http import JsonResponse
from django.shortcuts import render

from gameplan.models import Game


def index(request, game_id):
    return render(request, 'games/details.html')


def get_game_details(request, game_id):
    details = list(Game.objects.filter(game_id=game_id).values())

    return JsonResponse(details, safe=False)
