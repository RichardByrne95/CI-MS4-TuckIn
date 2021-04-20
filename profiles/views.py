from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from profiles.models import CustomerProfile
from .forms import CustomerProfileForm


@login_required
def customer_profile(request):
    profile = get_object_or_404(CustomerProfile, customer=request.user)

    if request.method == "POST":
        form = CustomerProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully")
        else:
            messages.error(request, 'Update failed. Please ensure the form is valid.')
    else:
        form = CustomerProfileForm(instance=profile)

    # orders = profile.orders.all()
    context = {
        'form': form,
        # 'orders': orders,
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
