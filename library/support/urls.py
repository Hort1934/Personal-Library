# support/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('support/', views.support, name='support'),
]
