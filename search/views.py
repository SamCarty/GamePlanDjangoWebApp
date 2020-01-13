from django.http import JsonResponse
from django.views.generic import ListView

from gameplan.models import Game


def search(request, title):
    if title != '':
        results = list(Game.objects.filter(title__icontains=title).values())

        if len(results) <= 10:
            return JsonResponse(results, safe=False)

    return JsonResponse('', safe=False)


class SearchResultsView(ListView):
    model = Game
    template_name = 'search/search.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return Game.objects.filter(title__icontains=query)
