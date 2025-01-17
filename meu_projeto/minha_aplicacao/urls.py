# minha_aplicacao/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Página inicial
    path('login/', views.login_view, name='login'),
    path('mfa_verify/', views.mfa_verify, name='mfa_verify'),
]
