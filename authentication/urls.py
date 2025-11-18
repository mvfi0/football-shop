from django.urls import path
from authentication.views import login, register, logout, whoami

app_name = 'authentication'

urlpatterns = [
    path('login/', login, name='login'),
    path('register/', register, name='register'),
    path('logout/', logout, name='logout'),
    path('whoami/', whoami, name='whoami'),
]