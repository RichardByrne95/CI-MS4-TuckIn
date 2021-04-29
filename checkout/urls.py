from django.urls import path
from . import views
from .webhooks import webhook

urlpatterns = [
    path('address/', views.checkout_address, name='checkout_address'),
    path('time/', views.checkout_time, name='checkout_time'),
    path('payment/', views.checkout_payment, name='checkout_payment'),
    path('order-confirmation/<order_number>/', views.order_confirmation, name='order_confirmation'),
    path('webhooks/', webhook, name='webhook'),
]
