from django.urls import path

from recommender import views

urlpatterns = [
    path('content-based/<str:game_id>/<int:n>', views.get_content_based_recommendations, name='similar_items'),
    path('bought-together/<str:game_id>/<int:n>', views.get_bought_together_recommendations, name='bought-together'),
    path('top-charts', views.get_top_charts_recommendations, name='top_charts')
]
