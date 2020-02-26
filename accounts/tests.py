from django.contrib.auth.models import User
from django.test import TestCase

from accounts.models import Wishlist, Dislike
from gameplan.models import Game


class AccountsTest(TestCase):

    @classmethod
    def setUp(cls):
        cls.user = User.objects.create(username='Test', password='test')
        cls.game = Game.objects.create(game_id=1)

    def test_new_user_created(self):
        self.assertTrue(User.objects.filter(username=self.user.username).exists(), "User not created.")

    def test_add_to_wishlist_adds(self):
        self.client.force_login(self.user)

        data = {'game_id': self.game.game_id,
                'attribute': 'wishlist'}
        self.client.post('/accounts/add-or-remove-attribute/', data)

        exists = Wishlist.objects.filter(user_id=self.user.id, game_id=self.game.game_id).values('game_id').exists()

        self.assertTrue(exists, "Title not added to wishlist.")

    def test_add_to_disliked_adds(self):
        self.client.force_login(self.user)

        data = {'game_id': self.game.game_id,
                'attribute': 'dislike'}
        self.client.post('/accounts/add-or-remove-attribute/', data)

        exists = Dislike.objects.filter(user_id=self.user.id, game_id=self.game.game_id).values('game_id').exists()

        self.assertEqual(True, exists, "Title not added to disliked.")
