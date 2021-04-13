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
            'address_1': request.POST['address_1'],
            'address_2': request.POST['address_2'],
        }
        request.session['address'] = form_data
    
    address_form = request.session.get('address')
    print(form_data)
    if address_form:
        context = {
            'address_form': address_form,
        }
    else:
        context = {}
    return render(request, 'checkout/checkout-time.html', context)


def checkout_payment(request):
    if request.method == "POST":
        delivery_time = request.POST.get('delivery_time')
        request.session['delivery_time'] = delivery_time

    address = request.session.get('address')
    delivery_time = request.session.get('delivery_time')
    bag = request.session.get('bag', {})

    order_form = OrderForm()
    context = {
        'order_form': order_form,
    }
    return render(request, 'checkout/checkout-payment.html', context)


def order_confirmation(request):
    context = {}
    return render(request, 'checkout/order_confirmation.html', context)
