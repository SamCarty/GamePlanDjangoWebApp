from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from gameplan.models import Game


def index(request):
    return render(request, 'gameplan/index.html')
