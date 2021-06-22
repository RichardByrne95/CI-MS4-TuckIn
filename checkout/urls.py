from . import views
from django.urls import path
from .webhooks import webhook

urlpatterns = [
    path('address/', views.checkout_address, name='checkout_address'),
    path('time/', views.checkout_time, name='checkout_time'),
    path('payment/', views.checkout_payment, name='checkout_payment'),
    path('order-confirmation/<order_number>/',
         views.order_confirmation, name='order_confirmation'),
    path('cache_checkout_data/', views.cache_checkout_data,
         name='cache_checkout_data'),
    path('wh/', webhook, name='webhook'),
]
