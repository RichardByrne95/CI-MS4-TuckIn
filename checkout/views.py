import json
import stripe
import datetime
from django.utils import timezone
from django.contrib import messages
from django.conf import settings
from django.http import HttpResponse
from .forms import OrderForm
from .models import Order, OrderLineItem
from profiles.models import CustomerProfile
from restaurants.models import FoodItem, Restaurant
from django.urls import reverse
from bag.contexts import bag_contents
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404, redirect, render


def checkout_address(request):
    # Create instance of order form with logged in user's details
    if request.user.is_authenticated:
        profile = get_object_or_404(CustomerProfile, customer=request.user)
        # Put saved details into fields
        address_form = OrderForm(initial={
            'full_name': profile.full_name,
            'email': profile.customer.email,
            'phone_number': profile.default_phone_number,
            'address_1': profile.default_address_1,
            'address_2': profile.default_address_2,
            'postcode': profile.default_postcode,
        })
        # Make email field readonly
        address_form.fields['email'].widget.attrs['readonly'] = True
    # If an address has been inputted via the homepage or location changer
    elif request.session['maps_address']:
        maps_address = request.session['maps_address'].split(',')
        address_form = OrderForm(initial={
            'full_name': "",
            'email': "",
            'phone_number': "",
            'address_1': maps_address[0].lstrip(),
            'address_2': maps_address[1].lstrip(),
            'postcode': "",
        })
        # Make email field readonly
        address_form.fields['email'].widget.attrs['readonly'] = False
    # Otherwise, create blank order form
    else:
        address_form = OrderForm()
    
    restaurant_name = request.session.get('restaurant')
    restaurant = get_object_or_404(Restaurant, name=restaurant_name)

    context = {
        'address_form': address_form,
        'restaurant': restaurant,
    }
    return render(request, 'checkout/checkout_address.html', context)


def checkout_time(request):
    # Add address data to session
    if request.method == "POST":
        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'address_1': request.POST['address_1'],
            'address_2': request.POST['address_2'],
            'postcode': request.POST['postcode'],
        }
        request.session['address'] = form_data

    # Get delivery times
    bag = request.session.get('bag', {})
    current_restaurant = get_object_or_404(Restaurant, name=list(bag)[0])
    delivery_times = current_restaurant.get_todays_delivery_times()

    # Get address form
    address_form = request.session.get('address')

    context = {
        'address_form': address_form,
        'delivery_times': delivery_times,
    }
    return render(request, 'checkout/checkout_time.html', context)


def checkout_payment(request):
    # Add selected delivery time to session
    if request.method == "POST":
        if 'from_delivery_time' in request.POST:
            delivery_time = request.POST.get('delivery_time')
            request.session['delivery_time'] = delivery_time
    
    # Get variables
    bag = request.session.get('bag')
    current_bag = bag_contents(request)
    now = timezone.now()

    # Format delivery time for processing
    session_delivery_time = str(request.session['delivery_time']).replace('.', '')

    # Get delivery time as datetime object
    # Format differently based on whether delivery time has minutes or not e.g. 7:30 pm vs 7 pm
    if len(session_delivery_time) <= 5:
        format = '%Y-%m-%d %I %p'
    else:
        format = '%Y-%m-%d %I:%M %p'
    delivery_time = datetime.datetime.strptime(f'{now.date()} {session_delivery_time}', format)

    # Make delivery time aware
    delivery_time = delivery_time.replace(tzinfo=timezone.utc)

    # Get restaurant associated with order
    restaurant = request.session.get('restaurant')
    order_restaurant = get_object_or_404(Restaurant, name=restaurant)


    # Handle submitting order
    if request.method == "POST":
        if 'from_delivery_time' not in request.POST:
            # Check if user changed delivery details on checkout page
            for item in request.POST:
                if item == "csrfmiddlewaretoken" or item == "city" or item == "save-info" or item == "client_secret" or item == "delivery_time" or item == "from_delivery_time":
                    pass
                else:
                    if request.POST[item] != request.session['address'][item]:
                        request.session['address'][item] = request.POST[item]
            # Create order form
            address_form = request.session.get('address')
            customer_profile = get_object_or_404(CustomerProfile, customer=request.user) if request.user.is_authenticated else None
            order_form = OrderForm({
                'full_name': address_form['full_name'],
                'email': address_form['email'],
                'phone_number': address_form['phone_number'],
                'address_1': address_form['address_1'],
                'address_2': address_form['address_2'],
                'city': 'Dublin',
                'postcode': address_form['postcode'],
            })

            # If valid, add additional fields not in form model and save order form
            if order_form.is_valid():
                order = order_form.save(commit=False)
                order.customer_profile = customer_profile
                order.order_restaurant = order_restaurant
                order.delivery_cost = current_bag['delivery_cost']
                order.delivery_time = delivery_time
                order.order_total  = current_bag['order_total']
                order.grand_total = current_bag['grand_total']
                order.original_bag = bag
                order.stripe_payment_id = request.POST.get('client_secret').split('_secret')[0]
                order.save()

                # Create line item for each food in bag
                for data in bag_contents(request)['bag_contents']:
                    try:
                        order_line_item = OrderLineItem(
                            order=order,
                            food_item=data['food'],
                            quantity=data['quantity'],
                        )
                        order_line_item.save()
                    except FoodItem.DoesNotExist:
                        messages.error(request, "Issue creating order line items.")
                        order.delete()
                        return redirect(reverse('view_bag'))
                
                return redirect(reverse('order_confirmation', args=[order.order_number]))
            # Else tell user about error
            else:
                messages.error(
                    request, "Order form either received incorrect data or did not receive all necessary fields.")
    
    # Generate Order Form
    if request.user.is_authenticated:
        # Create order form with saved profile details
        profile = get_object_or_404(CustomerProfile, customer=request.user)
        order_form = OrderForm({
            'full_name': profile.full_name,
            'email': profile.customer.email,
            'phone_number': profile.default_phone_number,
            'address_1': profile.default_address_1,
            'address_2': profile.default_address_2,
            'city': 'Dublin',
            'postcode': profile.default_postcode,
            'order_restaurant': order_restaurant,
        })
        # Raise error if form is invalid
        messages.error(request, "Order form is not accepting the inputted data.") if not order_form.is_valid() else None
    else:
        # Create order form using session data
        address_form = request.session.get('address')
        order_form = OrderForm({
            'full_name': address_form['full_name'],
            'email': address_form['email'],
            'phone_number': address_form['phone_number'],
            'address_1': address_form['address_1'],
            'address_2': address_form['address_2'],
            'city': 'Dublin',
            'postcode': address_form['postcode'],
        })
        # Raise error if form is invalid
        messages.error(
            request, "Order form is not accepting the inputted data.") if not order_form.is_valid() else None

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
    # Warning if stripe public key has not been set in environment variables
    if not settings.STRIPE_PUBLIC_KEY:
        messages.warning(request, 'Stripe public key is missing.')

    context = {
        'order_form': order_form,
        'delivery_time': delivery_time,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
        'client_secret': intent.client_secret,
    }
    return render(request, 'checkout/checkout_payment.html', context)


def order_confirmation(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)
    bag = request.session['bag']

    # Send success message to user
    messages.success(request, f'Order successfully sent to the restaurant! \
        Your order number is {order_number}. A confirmation email will be sent to {order.email}')
    
    # Remove the bag from the session
    # if 'bag' in request.session:
    #     del request.session['bag']

    context = {
        'order': order,
        'bag': bag,
    }
    return render(request, 'checkout/order_confirmation.html', context)


# Post additional order data (data that doesn't fit within the confirmCardPayment's 'payment_method') to the payment intent. 
# This allows the order instance in the db to be created when Stripe sends back the payment succeeded webhook.
@require_POST
def cache_checkout_data(request):
    try:
        payment_id = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(payment_id, metadata={
            'user': request.user,
            'save_info': request.POST.get('save_info'),
            'bag': json.dumps(request.session.get('bag', {})),
        })
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, 'Sorry, your payment cannot be processed right now. Please try again later.', status=400)
        return HttpResponse(content=e, status=400)
