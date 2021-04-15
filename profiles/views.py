from .forms import CustomerProfileForm
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def customer_profile(request):
    form = CustomerProfileForm()
    orders = None
    context = {
        'form': form,
        'orders': orders,
        'on_profile_page': True,
    }
    return render(request, 'profiles/customer_account.html', context)


@login_required
def customer_order_history(request):
    order = None
    context = {
        'order': order,
        'from_profile': True,
    }
    return render(request, 'profiles/customer_order_history.html', context)