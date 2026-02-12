from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('api/urls/', views.url_list_create, name='api_urls'),
    path('<str:slug>/', views.redirect_view, name='redirect'),
    
]