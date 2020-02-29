import sys

from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from accounts.models import Wishlist, Dislike
from gameplan.models import Game


class AccountsTest(TestCase):

    def setUp(self):
        User.objects.create_user(username='Test', password='test')
        self.user = User.objects.get()
        self.client = Client()
        self.client.force_login(self.user)
        self.game1 = Game.objects.create(game_id=1, first_release_date=100)
        self.game2 = Game.objects.create(game_id=2, first_release_date=20)

    def test_new_user_created(self):
        self.assertTrue(User.objects.filter(username='Test').exists(), "User not created.")

    def test_add_to_wishlist(self):
        data = {'game_id': self.game1.game_id,
                'attribute': 'wishlist'}
        self.client.post('/accounts/add-or-remove-attribute/', data)

        exists = Wishlist.objects.filter(user_id=self.user.id, game_id=self.game1.game_id).values('game_id').exists()
        self.assertTrue(exists, "Title not added to wishlist.")

    def test_remove_from_wishlist(self):
        data = {'game_id': self.game1.game_id,
                'attribute': 'wishlist'}
        self.client.post('/accounts/add-or-remove-attribute/', data)
        data = {'game_id': self.game1.game_id,
                'attribute': 'wishlist'}
        self.client.post('/accounts/add-or-remove-attribute/', data)

        exists = Wishlist.objects.filter(user_id=self.user.id, game_id=self.game1.game_id).values('game_id').exists()
        self.assertFalse(exists, "Title not removed from wishlist.")

    def test_add_to_disliked(self):
        data = {'game_id': self.game1.game_id,
                'attribute': 'dislike'}
        self.client.post('/accounts/add-or-remove-attribute/', data)

        exists = Dislike.objects.filter(user_id=self.user.id, game_id=self.game1.game_id).values('game_id').exists()
        self.assertTrue(exists, "Title not added to disliked.")

    def test_remove_from_disliked(self):
        data = {'game_id': self.game1.game_id,
                'attribute': 'dislike'}
        self.client.post('/accounts/add-or-remove-attribute/', data)
        data = {'game_id': self.game1.game_id,
                'attribute': 'dislike'}
        self.client.post('/accounts/add-or-remove-attribute/', data)

        exists = Dislike.objects.filter(user_id=self.user.id, game_id=self.game1.game_id).values('game_id').exists()
        self.assertFalse(exists, "Title not removed from disliked.")

    def test_wishlist_url(self):
        url = reverse('wishlist')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_wishlist_uses_correct_template(self):
        url = reverse('wishlist')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'accounts/wishlist.html')

    def test_wishlist_queryset(self):
        data = {'game_id': self.game1.game_id,
                'attribute': 'wishlist'}
        self.client.post('/accounts/add-or-remove-attribute/', data)
        data = {'game_id': self.game2.game_id,
                'attribute': 'wishlist'}
        self.client.post('/accounts/add-or-remove-attribute/', data)

        url = reverse('wishlist')
        response = self.client.get(url)

        self.assertTrue('game_list' in response.context_data)
        self.assertTrue(response.context_data['game_list'].filter(game_id=self.game1.game_id).exists(), "Wishlisted game 1 have not been returned in queryset")
        self.assertTrue(response.context_data['game_list'].filter(game_id=self.game1.game_id).exists(), "Wishlisted game 2 have not been returned in queryset")

    def test_signup_url(self):
        url = reverse('signup')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
