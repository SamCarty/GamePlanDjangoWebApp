from datetime import datetime

import pytz
from django.test import TestCase, Client
from django.urls import reverse

from accounts.models import User
from gatherer.models import Log
from import_games import import_max_range
from model_builder.bought_together_builder import recalculate_bought_together_db

import json


class RecommenderTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='Test1', password='test')
        self.user2 = User.objects.create_user(username='Test2', password='test')
        self.client = Client()
        self.client.force_login(self.user)

        import_max_range(20)
        self.game1_id = 4
        self.game2_id = 1182
        self.game3_id = 1121

    @staticmethod
    def create_log_item(content_id, event_type, session_id, user_id):
        return Log.objects.create(created=datetime.now(pytz.utc), content_id=content_id, event_type=event_type,
                                  session_id=session_id, user_id=user_id)

    def test_content_based_rec_json(self):
        url = reverse('similar_items', kwargs={'game_id': str(self.game1_id), 'n': 5})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200, 'Content-based recs should return HTML status code 200.')

        j = json.loads(response.content)
        self.assertEqual(j['original_game_id'], str(self.game1_id),
                         'Content-based recs not returning original game id.')

        data = j['data']
        self.assertEqual(len(data), 5, 'Length of returned games not equal to requested amount.')

        expected_games = {1182, 1305, 1121, 538, 1020}
        for game_id in expected_games:
            found = False
            for g in data:
                if str(game_id) == g['game_id']:
                    found = True
            self.assertTrue(found, 'Expected game ' + str(game_id) + ' not in content-based recommendations.')

    def test_bought_together(self):
        self.create_log_item(content_id=self.game1_id, event_type='purchase_event',
                             session_id=1234, user_id=self.user.id)
        self.create_log_item(content_id=self.game2_id, event_type='purchase_event',
                             session_id=1234, user_id=self.user.id)

        recalculate_bought_together_db()

        url = reverse('bought_together', kwargs={'game_id': str(self.game1_id), 'n': 5})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200, 'Bought-together recs should return HTML status code 200.')

        j = json.loads(response.content)
        self.assertEqual(j['original_game_id'], str(self.game1_id),
                         'Bought together recs not returning original game id.')

        data = j['data']
        self.assertEqual(str(self.game2_id), data[0]['game_id'], 'Expected game ' + str(self.game2_id) +
                         ' not in bought-together recommendations.')

    def test_like_you(self):
        self.create_log_item(content_id=self.game1_id, event_type='purchase_event',
                             session_id=1234, user_id=self.user.id)
        self.create_log_item(content_id=self.game2_id, event_type='purchase_event',
                             session_id=1234, user_id=self.user.id)
        self.create_log_item(content_id=self.game2_id, event_type='purchase_event',
                             session_id=5678, user_id=self.user2.id)
        self.create_log_item(content_id=self.game3_id, event_type='purchase_event',
                             session_id=5678, user_id=self.user2.id)

        recalculate_bought_together_db()

        url = reverse('like_you', kwargs={'n': 5})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200, 'Like you recs should return HTML status code 200.')

        j = json.loads(response.content)
        data = j['data']
        expected_games = {self.game1_id, self.game2_id, self.game3_id}
        for game_id in expected_games:
            found = False
            for g in data:
                if str(game_id) == g['game_id']:
                    found = True
            self.assertTrue(found, 'Expected game ' + str(game_id) + ' not in like you recommendations.')

    def test_similar_to_recent(self):
        self.create_log_item(content_id=self.game1_id, event_type='detail_view_event',
                             session_id=1234, user_id=self.user.id)

        url = reverse('similar_to_recent', kwargs={'n': 5})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200, 'Recent recs should return HTML status code 200.')

        j = json.loads(response.content)
        data = j['data']
        self.assertEqual(len(data), 5, 'Length of returned games not equal to requested amount.')

        expected_games = {1182, 1305, 1121, 538, 1020}
        for game_id in expected_games:
            found = False
            for g in data:
                if str(game_id) == g['game_id']:
                    found = True
            self.assertTrue(found, 'Expected game ' + str(game_id) + ' not in recent recommendations.')
