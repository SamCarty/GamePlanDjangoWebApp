from django.urls import path

from genres import views

urlpatterns = [
    path('get-all-genres/', views.get_all_genres, name='all_genres')
]
