# minha_aplicacao/urls.py

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),  # Página inicial
    path('about/', views.about, name='about'),  # Definindo a URL para 'about'
    path('contact/', views.contact, name='contact'),  # URL para a página de contato
    path('menu/', views.menu_view, name='menu'),
    path('item1/', views.item1_view, name='item1'),
    path('bebidas/', views.item2_view, name='bebidas'),
    path('sobre/', views.sobre_view, name='sobre'),
    path('item1_content/', views.item1_content, name='item1_content'),
    path('item2_content/', views.item2_content, name='item2_content'),
    path('item3_content/', views.item2_content, name='item3_content'),
    path('sobremesas/', views.sobremesas_view, name='sobremesas'),
    path('adicionar_sobremesa/', views.adicionar_sobremesa_view, name='adicionar_sobremesa'),  # Para adicionar sobremesa
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('mfa_verify/', views.mfa_verify_view, name='mfa_verify'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# if settings.DEBUG:  # Apenas em ambiente de desenvolvimento
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
