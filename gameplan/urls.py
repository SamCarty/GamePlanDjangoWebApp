from django.urls import path

from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='index'),
    path('search/a/<title>', views.search, name='search_autocomplete'),
    path('search/', views.SearchResultsView.as_view(), name='search_results')
]
