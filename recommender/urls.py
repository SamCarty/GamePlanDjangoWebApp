from django.urls import path

from recommender import views

urlpatterns = [
    path('content-based/<str:game_id>/<int:n>', views.get_content_based_recommendations, name='similar_items')
]
