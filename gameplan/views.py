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
    model = Game
    template_name = 'gameplan/search.html'

    def get_queryset(self):
        query = self.request.GET.get('q')

        games = Game.objects.filter(title__icontains=query)
        for game in games:
            frd = int(game.first_release_date)
            game.first_release_date = datetime.utcfromtimestamp(frd).strftime('%d/%m/%Y')

            game.platforms_human = list(Platform.objects.filter(
                platform_id__in=game.platforms.all().values_list('platform_id', flat=True)).values('name'))

        return games
