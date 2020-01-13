from django.urls import path
from accounts import views

urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('wishlist/', views.Wishlist.as_view(), name='wishlist'),
    path('on-wishlist/<int:game_id>', views.on_wishlist, name='on_wishlist'),
    path('add-or-remove-wishlist/', views.add_remove_wishlist, name='add_remove_wishlist')
]
