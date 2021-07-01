from checkout.models import Order
from django.contrib import messages
from .forms import CustomerProfileForm
from profiles.models import CustomerProfile
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required


@login_required
def customer_profile(request):
    profile = get_object_or_404(CustomerProfile, customer=request.user)

    if request.method == 'POST':
        form = CustomerProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(
                request, 'Update failed. Please ensure the form is valid.')
    else:
        form = CustomerProfileForm(instance=profile)

    context = {
        'form': form,
    }
    return render(request, 'profiles/customer_profile.html', context)


@login_required
def customer_order_history(request):
    profile = get_object_or_404(CustomerProfile, customer=request.user)
    orders = profile.orders.all().order_by('-date')

    context = {
        'orders': orders,
        'on_profile_page': True,
    }
    return render(request, 'profiles/customer_order_history.html', context)


@login_required
def order_confirmation_from_profile(request, order_number):
    # Get order
    order = get_object_or_404(Order, order_number=order_number)

    # Message notifying that this confirmation is from a past order.
    messages.info(
        request,
        f'This is a past confirmation for order number {order_number}. '
        'A confirmation email was sent on the order date.'
    )

    context = {
        'order': order,
        'from_profile': True,
        'dynamic_navbar': True,
    }

    return render(request, 'checkout/order_confirmation.html', context)
