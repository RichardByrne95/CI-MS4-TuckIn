from checkout.forms import OrderForm
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib import messages


def checkout(request):
    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, "There's nothing in your bag at the moment.")
        return redirect(reverse('restaurants'))
    
    order_form = OrderForm()
    context = {
        'order_form': order_form,
    }
    return render(request, 'checkout/checkout.html', context)
