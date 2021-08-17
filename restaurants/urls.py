from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_restaurants, name='restaurants'),
    path('<int:restaurant_id>/', views.restaurant_menu, name='restaurant_menu'),
    path('delete_restaurant/<int:restaurant_id>/',
         views.delete_restaurant, name='delete_restaurant'),
]
