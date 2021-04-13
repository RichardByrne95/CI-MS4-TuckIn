from checkout.models import Order
from checkout.forms import OrderForm
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib import messages


def checkout_address(request):
    address_form = OrderForm()
    context = {
        'address_form': address_form,
    }
    return render(request, 'checkout/checkout-address.html', context)


def checkout_time(request):
    if request.method == "POST":
        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'postcode': request.POST['postcode'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
        }
        request.session['form_data'] = form_data
    
    context = {}
    return render(request, 'checkout/checkout-time.html', context)


def checkout_payment(request):
    bag = request.session.get('bag', {})

    time = request.post.get('time')
    request.session['time'] = time

    order_form = OrderForm()
    context = {
        'order_form': order_form,
    }
    return render(request, 'checkout/checkout-payment.html', context)


def order_confirmation(request):
    context = {}
    return render(request, 'checkout/order_confirmation.html', context)
