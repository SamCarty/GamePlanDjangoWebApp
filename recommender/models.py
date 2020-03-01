from django.db import models

from gameplan.models import Game


class RecommendationPairing(models.Model):
    created = models.DateTimeField(null=True)
    from_game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="from_game")
    to_game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="to_game")
    support = models.FloatField(null=True)
    confidence = models.FloatField(null=True)

    def __str__(self):
        return self.from_game.title + " -> " + self.to_game.title + " support: " + str(self.support) + " confidence: "\
               + str(self.confidence)
