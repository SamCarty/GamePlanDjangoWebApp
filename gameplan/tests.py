from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from gameplan.models import Game


class GameplanTest(TestCase):

    def setUp(self):
        User.objects.create_user(username='Test', password='test')
        self.user = User.objects.get()
        self.client = Client()
        self.client.force_login(self.user)

        game_objects = ({'game_id': 1, 'title': 'Game 1', 'first_release_date': 0},
                       {'game_id': 2, 'title': 'Game 2', 'first_release_date': 0},
                       {'game_id': 3, 'title': 'Game 3', 'first_release_date': 0},
                       {'game_id': 4, 'title': 'Game 4', 'first_release_date': 0},
                       {'game_id': 5, 'title': 'Game 5', 'first_release_date': 0},
                       {'game_id': 6, 'title': 'Game 6', 'first_release_date': 0},
                       {'game_id': 7, 'title': 'Game 7', 'first_release_date': 0},
                       {'game_id': 8, 'title': 'Game 8', 'first_release_date': 0},
                       {'game_id': 9, 'title': 'Game 9', 'first_release_date': 0},
                       {'game_id': 10, 'title': 'Game 10', 'first_release_date': 0})

        for item in game_objects:
            Game.objects.create(game_id=item['game_id'], title=item['title'],
                                first_release_date=item['first_release_date'])

    def test_search_uses_correct_template(self):
        url = reverse('search_results') + '?q='
        response = self.client.get(url)

        self.assertTemplateUsed(response, 'gameplan/search.html', 'Search results does not use the search template')

    def test_search_get_genres(self):
        url = reverse('search_results') + '?q='
        response = self.client.get(url)
        self.assertTrue('genres' in response.context)

    def test_search_get_queryset(self):
        url = reverse('search_results') + '?q='
        response = self.client.get(url)

        self.assertTrue('search_results' in response.context)
        for game in Game.objects.all():
            self.assertTrue(game in response.context['search_results'].object_list,
                            'Game ' + game.game_id + ' has not been returned in queryset')

    def test_search_query_as_written(self):
        game = Game.objects.get(game_id=2)
        url = reverse('search_results') + '?q=' + game.title
        response = self.client.get(url)

        self.assertTrue('search_results' in response.context)
        self.assertTrue(game in response.context['search_results'].object_list,
                        'Game ' + game.game_id + ' has not been returned in queryset')

    def test_search_query_lower_case(self):
        game = Game.objects.get(game_id=2)
        url = reverse('search_results') + '?q=' + game.title.lower()
        response = self.client.get(url)

        self.assertTrue('search_results' in response.context)
        self.assertTrue(game in response.context['search_results'].object_list,
                        'Game ' + game.game_id + ' has not been returned in queryset')

    def test_search_query_substring(self):
        game = Game.objects.get(game_id=2)
        url = reverse('search_results') + '?q=2'
        response = self.client.get(url)

        self.assertTrue('search_results' in response.context)
        self.assertTrue(game in response.context['search_results'].object_list,
                        'Game ' + game.game_id + ' has not been returned in queryset')

    def test_search_query_multiple_results(self):
        url = reverse('search_results') + '?q=1'
        response = self.client.get(url)

        self.assertTrue('search_results' in response.context)
        for game in Game.objects.filter(title__contains=1):
            self.assertTrue(game in response.context['search_results'].object_list,
                            'Game ' + game.game_id + ' has not been returned in queryset')

    def test_home_uses_correct_template(self):
        url = reverse('index')
        response = self.client.get(url)

        self.assertTemplateUsed(response, 'gameplan/index.html', 'Home does not use the index template')

    def test_home_get_genres(self):
        url = reverse('index')
        response = self.client.get(url)
        self.assertTrue('genres' in response.context)
