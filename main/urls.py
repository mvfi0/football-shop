# main/urls.py
from django.urls import path
from .views import identity

urlpatterns = [
    path('', identity, name='identity'),
]
