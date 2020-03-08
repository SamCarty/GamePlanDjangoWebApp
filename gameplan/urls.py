from django.urls import path

from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='index'),
    path('search/a/<title>', views.search, name='search_autocomplete'),
    path('search/', views.SearchResultsView.as_view(), name='search_results'),
    path('loaderio-9810f09c6dab96eb6166d196409169e0/', views.loader_validation, name='loader')

]
