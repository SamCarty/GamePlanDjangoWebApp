from gameplan.models import Game


def generate_recommendations(n):
    games = Game.objects.order_by('-popularity')[:n].values()
    return games
