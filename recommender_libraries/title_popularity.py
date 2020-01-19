from gameplan.models import Game


def generate_recommendations(n):
    games = list(Game.objects.order_by('-popularity')[:n].values())
    return games
