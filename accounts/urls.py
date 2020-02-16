from django.urls import path
from accounts import views

urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('wishlist/', views.Wishlist.as_view(), name='wishlist'),
    path('check-attribute/<str:attribute>/<int:game_id>', views.check_attribute, name='check_attribute'),
    path('add-or-remove-attribute/', views.add_remove_attribute, name='add_remove_attribute')
]
