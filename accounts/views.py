import functools
import json
import sys

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views import generic

from gameplan.models import Game
from accounts.models import Wishlist as WishlistModel


class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


@method_decorator(login_required, name='dispatch')
class Wishlist(generic.ListView):
    model = Game
    template_name = 'accounts/wishlist.html'

    def get_queryset(self):
        user = self.request.user
        user_id = user.id

        game_ids = WishlistModel.objects.filter(user_id=user_id).values('game_id')
        print(game_ids, sys.stderr)

        games = Game.objects.filter(game_id__in=game_ids)
        print(games, sys.stderr)
        return games


@login_required
def on_wishlist(request, game_id):
    user = request.user
    user_id = user.id
    if WishlistModel.objects.filter(user_id=user_id, game_id=game_id).values('game_id').exists():
        return True
    else:
        return False


def add_remove_wishlist(request):
    if request.user.is_authenticated:
        response_data = {'auth': True}

        game_id = request.POST.get()
        user = request.user
        user_id = user.id
        game_ids = list(WishlistModel.objects.filter(user_id=user_id, game_id=game_id).values('game_id'))

        if game_ids:
            # remove it
            WishlistModel.objects.filter(user_id=request.user.id, game_id=game_id).delete()
            response_data['on_wishlist'] = False
        else:
            # add it
            WishlistModel.objects.create(user_id=request.user.id, game_id=game_id)
            response_data['on_wishlist'] = True

        return JsonResponse(response_data, safe=False)
    else:
        json.dumps({'auth': False})
        return JsonResponse(json.dumps({'auth': False}), safe=False)

