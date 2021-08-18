from . import views
from django.urls import path

urlpatterns = [
    path('list_your_restaurant/', views.list_your_restaurant,
         name='list_your_restaurant'),
    path('cookies_policy/', views.cookies_policy,
         name='cookies_policy'),
    path('privacy_policy/', views.privacy_policy,
         name='privacy_policy'),
    path('help/', views.help,
         name='help'),
]
