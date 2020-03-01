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

    def test_details_has_basic_details(self):
        game = Game.objects.get(game_id=4)
        url = reverse('game_details', kwargs={'game_id': game.game_id})
        response = self.client.get(url)

        self.assertTrue('game_details' in response.context)
        self.assertTrue(game.summary in response.context['game_details']['summary'],
                        'Summary has not been returned.')
        self.assertTrue(game.first_release_date in response.context['game_details']['first_release_date'],
                        'Release date has not been returned.')

    def test_details_has_extra_details(self):
        game = Game.objects.get(game_id=4)
        url = reverse('game_details', kwargs={'game_id': game.game_id})
        response = self.client.get(url)

        self.assertTrue('screenshots' in response.context)
        for screenshot in game.screenshots.all():
            found = False
            for s in response.context['screenshots']:
                if screenshot.screenshot_id == s['screenshot_id']:
                    found = True
            self.assertTrue(found, 'Screenshot ' + screenshot.screenshot_id + ' not in response.')

        self.assertTrue('involved_companies' in response.context)
        for company in game.involved_companies.select_related('company').all():
            found = False
            for c in response.context['involved_companies']:
                if company.company_id == c['company_id']:
                    found = True
            self.assertTrue(found, 'Company ' + company.company_id + ' not in response.')

        self.assertTrue('genres' in response.context)
        for genre in game.genres.all():
            found = False
            for g in response.context['game_genres']:
                if genre.genre_id == g['genre_id']:
                    found = True
            self.assertTrue(found, 'Genre ' + genre.genre_id + ' not in response.')

        self.assertTrue('platforms' in response.context)
        for platform in game.platforms.all():
            found = False
            for s in response.context['platforms']:
                if platform.platform_id == s['platform_id']:
                    found = True
            self.assertTrue(found, 'Platform ' + platform.platform_id + ' not in response.')

