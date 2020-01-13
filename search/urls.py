from django.urls import path

from search import views

urlpatterns = [
    path('a/<str:title>', views.search, name='search_autocomplete'),
    path('', views.SearchResultsView.as_view(), name='search_results')
]
