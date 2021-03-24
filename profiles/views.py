from .models import CustomerProfile
from django.shortcuts import get_object_or_404, render

# Create your views here.
def customer_profile(request):
    form = None
    orders = None
    context = {
        'form': form,
        'orders': orders,
        'on_profile_page': True,
    }
    return render(request, 'profiles/customer_account.html', context)


def customer_order_history(request):
    order = None
    context = {
        'order': order,
        'from_profile': True,
    }
    return render(request, 'profiles/customer_order_history.html', context)