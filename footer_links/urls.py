from django.urls import path
from . import views

urlpatterns = [
    path('list_your_restaurant/', views.list_your_restaurant,
         name='list_your_restaurant'),
]
