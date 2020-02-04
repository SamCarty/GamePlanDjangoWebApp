from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import TemplateView

from gameplan.views import get_all_genres
from accounts.views import on_wishlist
from gameplan.models import Game, Screenshot, InvolvedCompany, Company, Genre, Platform
from gameplan.views import create_session


class GameDetails(TemplateView):
    template_name = 'games/details.html'

    def get(self, request, *args, **kwargs):
        context = dict()
        context['session_id'] = create_session(request)
        context['genres'] = get_all_genres()

        return render(request, self.template_name, context)


def get_game_details(request, game_id):
    details = list(Game.objects.filter(game_id=game_id).values())
    details[0]['screenshots'] = get_screenshots_by_game_id(request, game_id)
    details[0]['involved_companies'] = get_involved_companies_by_game_id(request, game_id)
    details[0]['genres'] = get_genres_by_game_id(request, game_id)
    details[0]['platform'] = get_platforms_by_game_id(request, game_id)

    if request.user.is_authenticated:
        details[0]['on_wishlist'] = on_wishlist(request, game_id)

    return JsonResponse(details, safe=False)


def get_screenshots_by_game_id(request, game_id):
    screenshot_ids = list(Game.screenshots.through.objects.filter(game_id=game_id).values())

    ids = list()
    for item in screenshot_ids:
        ids.append(str(item['screenshot_id']))

    urls = list(Screenshot.objects.filter(screenshot_id__in=ids).values())

    return urls


def get_involved_companies_by_game_id(request, game_id):
    involved_company_ids = list(Game.involved_companies.through.objects.filter(game_id=game_id).values())

    # Get all the involved company objects
    ids = list()
    for item in involved_company_ids:
        ids.append(str(item['involvedcompany_id']))
    involved_companies = list(InvolvedCompany.objects.filter(involved_company_id__in=ids).values())

    # Get all the company objects
    ids = list()
    for item in involved_companies:
        ids.append(str(item['company_id']))
    companies = list(Company.objects.filter(company_id__in=ids).values())

    # Append the company role to the company
    for idx, company in enumerate(companies):
        involved_company = next((item for item in involved_companies if item["company_id"] == company['company_id']),
                                None)
        company['is_dev'] = involved_company['developer']
        company['is_pub'] = involved_company['publisher']

    return companies


def get_genres_by_game_id(request, game_id):
    genre_ids = list(Game.genres.through.objects.filter(game_id=game_id).values())

    ids = list()
    for item in genre_ids:
        ids.append(str(item['genre_id']))

    genres = list(Genre.objects.filter(genre_id__in=ids).values())

    return genres


def get_platforms_by_game_id(request, game_id):
    platform_ids = list(Game.platforms.through.objects.filter(game_id=game_id).values())

    ids = list()
    for item in platform_ids:
        ids.append(str(item['platform_id']))

    platforms = list(Platform.objects.filter(platform_id__in=ids).values())

    return platforms
