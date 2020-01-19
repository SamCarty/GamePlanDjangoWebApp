from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.views.generic import ListView

from recommender.views import get_top_charts_recommendations
from gameplan.models import Game


class HomePageView(TemplateView):
    template_name = 'gameplan/index.html'

    def get(self, request, *args, **kwargs):
        context = dict()
        context['top_charts'] = get_top_charts_recommendations(request, 10)
        return render(request, self.template_name, context)


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
