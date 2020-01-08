from django.urls import path

from search import views

urlpatterns = [
    path('<str:title>', views.search, name='search')
]
