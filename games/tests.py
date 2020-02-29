from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from gameplan.models import Game
from import_games import import_max_range


class GamesTest(TestCase):

    def setUp(self):
        User.objects.create_user(username='Test', password='test')
        self.user = User.objects.get()
        self.client = Client()
        self.client.force_login(self.user)

        import_max_range(20)

    def test_details_url(self):
        url = reverse('game_details', kwargs={'game_id': 4})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200, 'Details should return HTML status code 200.')

    def test_details_uses_correct_template(self):
        url = reverse('game_details', kwargs={'game_id': 4})
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'games/details.html', 'Game details does not use the details template')

    def test_details_get_genres(self):
        url = reverse('game_details', kwargs={'game_id': 4})
        response = self.client.get(url)
        self.assertTrue('genres' in response.context)

    def test_details_has_all_information(self):
        game = Game.objects.get(game_id=4)
        url = reverse('game_details', kwargs={'game_id': game.game_id})
        response = self.client.get(url)

        self.assertTrue('screenshots' in response.context)
        self.assertTrue('involved_companies' in response.context)
        self.assertTrue('genres' in response.context)
        self.assertTrue('platform' in response.context)
        self.assertTrue('game_details' in response.context)
