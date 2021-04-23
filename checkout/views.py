from django.shortcuts import get_object_or_404, render
from bag.contexts import bag_contents
from django.conf import settings
from restaurants.models import Restaurant
from checkout.forms import OrderForm
from profiles.models import CustomerProfile
from django.contrib import messages
import stripe


def checkout_address(request):
    # Create instance of order form
    if request.user.is_authenticated:
        profile = get_object_or_404(CustomerProfile, customer=request.user)
        # Put saved details into fields
        address_form = OrderForm(initial={
            'full_name': profile.full_name,
            'email': profile.customer.email,
            'phone_number': profile.default_phone_number,
            'postcode': profile.default_postcode,
            'address_1': profile.default_address_1,
            'address_2': profile.default_address_2,
        })
        address_form.save(commit=False)
    else:
        address_form = OrderForm()

    context = {
        'address_form': address_form,
    }
    return render(request, 'checkout/checkout_address.html', context)


def checkout_time(request):
    # Add address data to session
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

        # Add restuarant name to session
        bag = request.session.get('bag', {})
        restaurant = list(bag.keys())
        request.session['restaurant'] = restaurant[0]

    # Get variables
    address_form = request.session.get('address')

    context = {
        'address_form': address_form,
    }
    return render(request, 'checkout/checkout_time.html', context)


def checkout_payment(request):
    # Add selected delivery time to session
    bag = request.session.get('bag', {})
    if request.method == "POST" and 'delivery_time' in request.POST:
        delivery_time = request.POST.get('delivery_time')
        request.session['delivery_time'] = delivery_time
    
    # Get restaurant associated with order
    restaurant = request.session.get('restaurant')
    order_restaurant = get_object_or_404(Restaurant, name=restaurant)
    
    # Generate Order Form
    if request.user.is_authenticated:
        profile = get_object_or_404(CustomerProfile, customer=request.user)
        # Create order form with saved profile details
        order_form = OrderForm(initial={
            'full_name': profile.full_name,
            'email': profile.customer.email,
            'phone_number': profile.default_phone_number,
            'postcode': profile.default_postcode,
            'address_1': profile.default_address_1,
            'address_2': profile.default_address_2,
            'order_restaurant': order_restaurant,
        })
        order_form.save(commit=False)
    else:
        # Create order form using session data
        address_form = request.session.get('address')
        order_form = OrderForm(initial={
            'full_name': address_form['full_name'],
            'email': address_form['email'],
            'phone_number': address_form['phone_number'],
            'postcode': address_form['postcode'],
            'address_1': address_form['address_1'],
            'address_2': address_form['address_2'],
            'order_restaurant': order_restaurant,
        })
        order_form.save(commit=False)

    # Get variables
    delivery_time = request.session.get('delivery_time')
    current_bag = bag_contents(request)
    total = current_bag['grand_total']

    # Stripe
    stripe_total = round(total * 100) # Stripe requires an integer when charging
    stripe.api_key = settings.STRIPE_SECRET_KEY
    intent = stripe.PaymentIntent.create(
        amount=stripe_total,
        currency=settings.STRIPE_CURRENCY,
    )
    if not settings.STRIPE_PUBLIC_KEY:
        messages.warning(request, 'Stripe public key is missing.')

    context = {
        'order_form': order_form,
        'delivery_time': delivery_time,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
        'client_secret': intent.client_secret,
    }
    return render(request, 'checkout/checkout_payment.html', context)


def order_confirmation(request):
    context = {}
    return render(request, 'checkout/order_confirmation.html', context)
