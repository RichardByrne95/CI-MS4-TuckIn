from checkout.models import Order
from django.contrib import messages
from django.urls.base import reverse
from .forms import CustomerProfileForm
from profiles.models import CustomerProfile
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render


@login_required
def customer_profile(request):
    try:
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

    except Exception:
        messages.error(
            request, 'Oops! Looks like an error occurred. Please try again. If this error persists, please contact us via the help section.', status=400)
        return redirect(reverse('home'))


@login_required
def customer_order_history(request):
    try:
        profile = get_object_or_404(CustomerProfile, customer=request.user)
        orders = profile.orders.all().order_by('-date')

        context = {
            'orders': orders,
            'on_profile_page': True,
        }
        return render(request, 'profiles/customer_order_history.html', context)
    except Exception:
        messages.error(
            request, 'Oops! Looks like an error occurred. Please try again. If this error persists, please contact us via the help section.', status=400)
        return redirect(reverse('home'))


@login_required
def order_confirmation_from_profile(request, order_number):
    try:
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
    except Exception:
        messages.error(
            request, 'Oops! Looks like an error occurred. Please try again. If this error persists, please contact us via the help section.')
        return redirect(reverse('home'))
