from django.urls import path

from recommender import views

urlpatterns = [
    path('content-based/<str:game_id>/<int:n>', views.get_content_based_recommendations_json, name='similar_items'),
    path('bought-together/<str:game_id>/<int:n>', views.get_bought_together_recommendations, name='bought_together'),
    path('like-you/<int:n>', views.get_users_like_you_recommendations, name='like_you'),
    path('similar-to-recent/<int:n>', views.get_similar_to_recent_recommendations, name='similar_to_recent'),
    path('top-charts', views.get_top_charts_recommendations, name='top_charts'),
    path('top-genre/<str:genre_id>/<int:n>', views.get_top_genre_recommendations, name='top_genre'),
    path('random/<int:n>', views.get_random_recommendations, name='random'),
    path('coming-soon/<int:n>', views.get_coming_soon_recommendations, name='coming_soon')
]
