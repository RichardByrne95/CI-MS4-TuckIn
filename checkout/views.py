from django.shortcuts import get_object_or_404, render
from bag.contexts import bag_contents
from profiles.models import CustomerProfile
from checkout.models import OrderLineItem
from restaurants.models import Restaurant
from checkout.forms import OrderForm
from django.conf import settings
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
    bag = request.session.get('bag')
    current_bag = bag_contents(request)

    # Get restaurant associated with order
    restaurant = request.session.get('restaurant')
    order_restaurant = get_object_or_404(Restaurant, name=restaurant)
    
    if request.method == "POST":
        # Add selected delivery time to session
        if 'delivery_time' in request.POST:
            delivery_time = request.POST.get('delivery_time')
            request.session['delivery_time'] = delivery_time

        # Handle submitting order
        elif 'delivery_time' not in request.POST:
            address_form = request.session.get('address')
            order_form = OrderForm(request.POST, initial={
                'full_name': address_form['full_name'],
                'email': address_form['email'],
                'phone_number': address_form['phone_number'],
                'address_1': address_form['address_1'],
                'address_2': address_form['address_2'],
                'postcode': address_form['postcode'],
                'city': 'Dublin',
                # 'order_restaurant': order_restaurant,
                # 'delivery_cost': current_bag['delivery_cost'],
                # 'order_total': current_bag['order_total'],
                # 'grand_total': current_bag['grand_total'],
                # 'original_bag': bag,
            })
            # If valid, save order form
            if order_form.is_valid():
                order = order_form.save()

                # Create line item for each food in bag
                for data in bag_contents(request)['bag_contents']:
                    try:
                        order_line_item = OrderLineItem(
                            order=order,
                            food_item=data['food'],
                            quantity=data['quantity'],
                        )
                        order_line_item.save()
                    except:
                        messages.error(request, "Issue creating order line items")
            # Else tell user about error
            else:
                messages.error(
                    request, "Order form either received incorrect data or did not receive all necessary fields.")
    
    # Generate Order Form
    if request.user.is_authenticated:
        profile = get_object_or_404(CustomerProfile, customer=request.user)
        # Create order form with saved profile details
        order_form = OrderForm(request.POST, initial={
            'full_name': profile.full_name,
            'email': profile.customer.email,
            'phone_number': profile.default_phone_number,
            'address_1': profile.default_address_1,
            'address_2': profile.default_address_2,
            'postcode': profile.default_postcode,
            'city': 'Dublin',
            # 'order_restaurant': order_restaurant,
        })
        if order_form.is_valid():
            order_form.save(commit=False)
        else:
            messages.error(request, "Order form is not accepting the inputted data.")
    else:
        # Create order form using session data
        address_form = request.session.get('address')
        order_form_data = {
            'full_name': address_form['full_name'],
            'email': address_form['email'],
            'phone_number': address_form['phone_number'],
            'address_1': address_form['address_1'],
            'address_2': address_form['address_2'],
            'postcode': address_form['postcode'],
            'city': 'Dublin',
        }
        order_form = OrderForm(order_form_data)
        if order_form.is_valid():
            order_form.save()
        else:
            messages.error(request, "Order form is not accepting the inputted data.")

    # Get variables
    delivery_time = request.POST.get('delivery_time')
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
