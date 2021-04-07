from checkout.forms import OrderForm
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib import messages


def checkout(request):
    bag = request.session.get('bag', {})
    
    order_form = OrderForm()
    context = {
        'order_form': order_form,
    }
    return render(request, 'checkout/checkout.html', context)


def order_confirmation(request):
    context = {}
    return render(request, 'checkout/order_confirmation.html', context)