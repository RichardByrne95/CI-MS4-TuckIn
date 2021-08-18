from . import views
from django.urls import path

urlpatterns = [
    path('', views.view_bag, name='view_bag'),
    path('add/', views.add_to_bag, name='add_to_bag'),
    path('remove/<food_id>/', views.remove_from_bag, name='remove_from_bag'),
    path('order_again/<order_number>/', views.order_again, name='order_again'),
]
