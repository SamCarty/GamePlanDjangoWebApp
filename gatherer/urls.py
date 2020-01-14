from django.urls import path

from gatherer import views

urlpatterns = [
    path('log-event/', views.log_event, name='log_event')
]
