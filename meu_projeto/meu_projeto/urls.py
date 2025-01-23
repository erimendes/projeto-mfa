# meu_projeto/meu_projeto/urls.py
"""
URL configuration for meu_projeto project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from minha_aplicacao import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    # path('about/', views.mfa_verify_view, name='about'),
    path('mfa_verify/', views.mfa_verify_view, name='mfa_verify'),
    path('accounts/login/', views.login_view, name='login'),
    # path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('logado/', views.logado_view, name='logado'),  # Adicione esta linha
    path('minha_aplicacao/', include('minha_aplicacao.urls')),
]
