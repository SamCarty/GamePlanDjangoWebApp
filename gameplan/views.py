from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.views.generic import ListView

from recommender.views import get_top_charts_recommendations
from gameplan.models import Game, Genre


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
        request.session.create().set_expiry(0)

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
        query = self.request.GET.get()
        return Game.objects.filter(title__icontains=query)
