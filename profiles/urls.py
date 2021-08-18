from . import views
from django.urls import path

urlpatterns = [
    path('', views.customer_profile, name='customer_profile'),
    path('customer_order_history/', views.customer_order_history,
         name='customer_order_history'),
    path('customer_order_history/<order_number>', views.order_confirmation_from_profile,
         name='order_confirmation_from_profile'),
]
