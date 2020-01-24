from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.views.generic import ListView
from datetime import datetime

from recommender.views import get_top_charts_recommendations
from gameplan.models import Game, Genre, Platform


class HomePageView(TemplateView):
    template_name = 'gameplan/index.html'

    def get(self, request, *args, **kwargs):
        context = dict()
        context['session_id'] = create_session(request)
        context['genres'] = get_all_genres()
        context['top_charts'] = get_top_charts_recommendations(request, 10)

        return render(request, self.template_name, context)


def create_session(request):
    if not request.session.session_key:
        request.session.create()
        request.session.set_expiry(0)

    return request.session.session_key


def get_all_genres():
    return Genre.objects.order_by('name').values()


def search(request, title):
    if title != '':
        results = list(Game.objects.filter(title__icontains=title).values())

        if len(results) <= 10:
            return JsonResponse(results, safe=False)

    return JsonResponse('', safe=False)


class SearchResultsView(ListView):
    paginate_by = 6
    model = Game
    template_name = 'gameplan/search.html'

    def get(self, request, *args, **kwargs):
        context = dict()
        context['session_id'] = create_session(request)
        context['genres'] = get_all_genres()

        platforms = list()
        genres = list()

        query = self.request.GET.get('q')
        games = Game.objects.filter(title__icontains=query)
        if self.request.GET.get('p') is not None:
            q_platforms = self.request.GET.get('p')
            q_platforms_list = [int(x) for x in q_platforms.split(',')]
            games = games.filter(platforms__platform_id__in=q_platforms_list)
        if self.request.GET.get('g') is not None:
            q_genres = self.request.GET.get('g')
            q_genres_list = [int(x) for x in q_genres.split(',')]
            games = games.filter(genres__genre_id__in=q_genres_list)

        for game in games:
            frd = int(game.first_release_date)
            game.first_release_date = datetime.utcfromtimestamp(frd).strftime('%d/%m/%Y')

            platforms_full = list(Platform.objects.filter(
                platform_id__in=game.platforms.all().values_list('platform_id', flat=True)).values('name',
                                                                                                   'platform_id'))

            game.platforms_full = platforms_full
            for platform in platforms_full:
                if platform not in platforms:
                    platforms.append(platform)

            genres_full = list(Genre.objects.filter(
                genre_id__in=game.genres.all().values_list('genre_id', flat=True)).values('name', 'genre_id'))

            game.genres_full = genres_full
            for genre in genres_full:
                if genre not in genres:
                    genres.append(genre)

        context['search_results_platforms'] = platforms
        context['search_results_genres'] = genres

        page = request.GET.get('page', 1)
        paginator = Paginator(games, 12)
        try:
            games_page = paginator.page(page)
        except PageNotAnInteger:
            games_page = paginator.page(1)
        except EmptyPage:
            games_page = paginator.page(paginator.num_pages)

        context['search_results'] = games_page

        return render(request, self.template_name, context)
