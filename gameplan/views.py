from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.views.generic import ListView
from datetime import datetime
from gameplan.filters import GameFilter

from recommender.views import get_top_charts_recommendations, get_recommender_categories
from gameplan.models import Game, Genre, Platform


class HomePageView(TemplateView):
    template_name = 'gameplan/index.html'

    def get(self, request, *args, **kwargs):
        context = dict()
        context['session_id'] = create_session(request)
        context['genres'] = get_all_genres()
        context['top_charts'] = get_top_charts_recommendations(request, 10)
        context['recommender_categories'] = get_recommender_categories(request)

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
    model = Game
    template_name = 'gameplan/search.html'

    def get(self, request, *args, **kwargs):
        context = dict()
        context['session_id'] = create_session(request)
        context['genres'] = get_all_genres()

        filter_set = GameFilter(self.request.GET, queryset=Game.objects.all())
        context['filter'] = filter_set
        games = filter_set.qs
        games = games.order_by('-first_release_date')

        for game in games:
            frd = int(game.first_release_date)
            game.first_release_date = datetime.utcfromtimestamp(frd).strftime('%d/%m/%Y')

            platforms_full = list(Platform.objects.filter(
                platform_id__in=game.platforms.all().values_list('platform_id', flat=True))
                                  .values('name', 'platform_id'))
            game.platforms_full = platforms_full

            genres_full = list(Genre.objects.filter(
                genre_id__in=game.genres.all().values_list('genre_id', flat=True))
                               .values('name', 'genre_id'))
            game.genres_full = genres_full

        context['search_results'] = self.setup_pagination(request, games)
        context['url_extension'] = self.get_url_extension(request)

        return render(request, self.template_name, context)

    @staticmethod
    def setup_pagination(request, data):
        page = request.GET.get('page', 1)
        paginator = Paginator(data, 12)
        try:
            games_page = paginator.page(page)
        except PageNotAnInteger:
            games_page = paginator.page(1)
        except EmptyPage:
            games_page = paginator.page(paginator.num_pages)

        return games_page

    @staticmethod
    def get_url_extension(request):
        p = ''
        if request.GET.get('platforms') is not None:
            for platform in request.GET.getlist('platforms'):
                p += '&platforms=' + platform

        g = ''
        if request.GET.get('genres') is not None:
            for genre in request.GET.getlist('genres'):
                g += '&genres=' + genre

        q = '&q=' + request.GET.get('q')

        return q + p + g