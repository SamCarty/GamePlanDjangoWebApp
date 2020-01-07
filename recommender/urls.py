from django.conf.urls import url
from django.urls import path

from recommender import views

urlpatterns = [
    path('content-based/<str:title>/', views.get_content_based_recommendations, name='similar_items')
]
