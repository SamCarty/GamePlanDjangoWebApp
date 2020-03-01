import time

from django.test import TestCase, Client
from django.urls import reverse

from accounts.models import User
from gatherer.models import Log, UserRating
from gameplan.models import Game
from recommender.models import RecommendationPairing


class GathererTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='Test', password='test')
        self.client = Client()
        self.client.force_login(self.user)

        self.game1 = Game.objects.create(game_id=1, title='Game 1')
        self.game2 = Game.objects.create(game_id=2, title='Game 2')

    def test_log_event(self):
        data = {'content_id': 1,
                'event_type': 'purchase_event',
                'session_id': 1234}
        self.client.post(reverse('log_event'), data)
        exists = Log.objects.get(user_id=self.user.id, content_id=1).event_type == 'purchase_event'
        self.assertTrue(exists, 'Gatherer did not save purchase event.')

    def test_ratings_recalculated_after_log(self):
        data = {'content_id': 1,
                'event_type': 'purchase_event',
                'session_id': 1234}
        self.client.post(reverse('log_event'), data)

        time.sleep(2)  # wait to give async time to calculate

        exists = UserRating.objects.count() > 0
        self.assertTrue(exists, 'User ratings were not recalculated after a log was filed.')
        self.assertEqual(UserRating.objects.get(user_id=self.user.id).user_rating, 10.0,
                         'User rating not calculated correctly.')

    def test_pairings_recalculated_after_log(self):
        data = {'content_id': self.game1.game_id,
                'event_type': 'purchase_event',
                'session_id': 1234}
        self.client.post(reverse('log_event'), data)

        data = {'content_id': self.game2.game_id,
                'event_type': 'purchase_event',
                'session_id': 1234}
        self.client.post(reverse('log_event'), data)

        time.sleep(2)  # wait to give async time to calculate

        exists = RecommendationPairing.objects.count() > 0
        self.assertTrue(exists, 'Recommendation pairings were not recalculated after a log was filed.')
        self.assertEqual(RecommendationPairing.objects.get(from_game=self.game1.game_id).to_game.game_id,
                         str(self.game2.game_id),
                         'Recommendation pairing not setup between game 1 -> game 2.')
        self.assertEqual(RecommendationPairing.objects.get(from_game=self.game2.game_id).to_game.game_id,
                         str(self.game1.game_id),
                         'Recommendation pairing not setup between game 2 -> game 1.')
