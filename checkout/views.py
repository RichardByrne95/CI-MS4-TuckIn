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
from profiles.forms import CustomerProfileForm
from restaurants.models import FoodItem, Restaurant
from django.urls import reverse
from bag.contexts import bag_contents
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404, redirect, render


@require_POST
def checkout_address(request):
    

    # Get restaurant
    restaurant_name = request.session.get('restaurant')
    restaurant = get_object_or_404(Restaurant, name=restaurant_name)

    # Prevent user checking out when restaurant is closed
    if not restaurant.is_open_now():
        messages.error(request, 'The restaurant is currently closed.')
        return redirect(reverse('view_bag'))

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
    elif 'maps_address' in request.session and request.session['maps_address']:
        maps_address = request.session['maps_address'].split(',')
        address_form = OrderForm(initial={
            'full_name': '',
            'email': '',
            'phone_number': '',
            'address_1': maps_address[0].lstrip(),
            'address_2': maps_address[1].lstrip(),
            'postcode': '',
        })
        # Make email field readonly
        address_form.fields['email'].widget.attrs['readonly'] = False
    # Otherwise, create blank order form
    else:
        address_form = OrderForm()

    context = {
        'address_form': address_form,
        'restaurant': restaurant,
    }
    return render(request, 'checkout/checkout_address.html', context)


@require_POST
def checkout_time(request):
    # Get delivery times
    bag = request.session.get('bag', {})
    current_restaurant = get_object_or_404(Restaurant, name=list(bag)[0])
    delivery_times = current_restaurant.get_todays_delivery_times()

    # Prevent user checking out when restaurant is closed
    if not current_restaurant.is_open_now():
        messages.error(request, 'The restaurant is currently closed.')
        return redirect(reverse('view_bag'))

    # Add address data to session
    if request.method == 'POST':
        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'address_1': request.POST['address_1'],
            'address_2': request.POST['address_2'],
            'postcode': request.POST['postcode'],
        }
        request.session['address'] = form_data

    # Get address form
    address_form = request.session.get('address')

    context = {
        'address_form': address_form,
        'delivery_times': delivery_times,
    }
    return render(request, 'checkout/checkout_time.html', context)


@require_POST
def checkout_payment(request):
    # Get restaurant associated with order
    restaurant = request.session.get('restaurant')
    order_restaurant = get_object_or_404(Restaurant, name=restaurant)

    # Prevent user checking out when restaurant is closed
    if not order_restaurant.is_open_now():
        messages.error(request, 'The restaurant is currently closed.')
        return redirect(reverse('view_bag'))

    # Add selected delivery time to session
    if request.method == 'POST':
        if 'from_delivery_time' in request.POST:
            delivery_time = request.POST.get('delivery_time')
            request.session['delivery_time'] = delivery_time

    # Get variables
    bag = request.session.get('bag')
    current_bag = bag_contents(request)
    now = timezone.now()

    # Format delivery time for processing
    session_delivery_time = str(
        request.session['delivery_time']).replace('.', '')

    # Get delivery time as datetime object
    if session_delivery_time == 'noon':
        session_delivery_time = '12 pm'
    elif session_delivery_time == 'midnight':
        session_delivery_time = '12 am'
    # Format differently based on whether delivery time has minutes or not e.g. 7:30 pm vs 7 pm
    if len(session_delivery_time) <= 5:
        format = '%Y-%m-%d %I %p'
    else:
        format = '%Y-%m-%d %I:%M %p'
    delivery_time = datetime.datetime.strptime(
        f'{now.date()} {session_delivery_time}', format)

    # Make delivery time aware
    delivery_time = delivery_time.replace(tzinfo=timezone.utc)

    # Handle submitting order
    if request.method == 'POST':
        if 'from_delivery_time' not in request.POST:
            # Check if user changed delivery details on checkout page
            for item in request.POST:
                if item == 'csrfmiddlewaretoken' or item == 'city' or item == 'save-info' or item == 'client_secret' or item == 'delivery_time' or item == 'from_delivery_time':
                    pass
                else:
                    if request.POST[item] != request.session['address'][item]:
                        request.session['address'][item] = request.POST[item]

            # Create order form
            address_form = request.session.get('address')
            customer_profile = get_object_or_404(
                CustomerProfile, customer=request.user) if request.user.is_authenticated else None
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
                order.order_total = current_bag['order_total']
                order.grand_total = current_bag['grand_total']
                order.original_bag = json.dumps(bag)
                order.stripe_payment_id = request.POST.get(
                    'client_secret').split('_secret')[0]
                order.save()

                # Create line item for each food in bag
                for data in bag_contents(request)['bag_contents']:
                    try:
                        order_line_item = OrderLineItem(
                            order=order,
                            food_item=data['food'],
                            quantity=data['quantity'],
                            additional_details=data['additional_details'],
                        )
                        order_line_item.save()
                    except FoodItem.DoesNotExist:
                        messages.error(
                            request, 'Issue creating order line items.')
                        order.delete()
                        return redirect(reverse('view_bag'))

                # Save the info to the user's profile
                request.session['save_info'] = 'save-info' in request.POST
                return redirect(reverse('order_confirmation', args=[order.order_number]))
            # Else tell user about error
            else:
                messages.error(
                    request, 'Order form either received incorrect data or did not receive all necessary fields.')

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
        messages.error(
            request, 'Order form is not accepting the inputted data.') if not order_form.is_valid() else None
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
            request, 'Order form is not accepting the inputted data.') if not order_form.is_valid() else None

    # Get variables
    delivery_time = request.POST.get('delivery_time')
    current_bag = bag_contents(request)
    total = current_bag['grand_total']

    # Stripe
    # Stripe requires an integer when charging
    stripe_total = round(total * 100)
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
        'order_restaurant': order_restaurant,
        'delivery_time': delivery_time,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
        'client_secret': intent.client_secret,
    }
    return render(request, 'checkout/checkout_payment.html', context)


def order_confirmation(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)
    save_info = request.session.get('save_info')

    if request.method == 'POST':
        try:
            rating = request.POST.get('rating')
            order.rating = rating
            order.save()
            order.order_restaurant.update_rating()
            messages.success(request, "Your rating has been saved!")
        except Exception:
            messages.error(
                request, "Could not save rating. Please try again later.")

    if request.user.is_authenticated:
        profile = get_object_or_404(CustomerProfile, customer=request.user)
        # Save the user's info
        if save_info:
            profile_data = {
                'email': order.email,
                'full_name': order.full_name,
                'default_phone_number': order.phone_number,
                'default_postcode': order.postcode,
                'default_city': order.city,
                'default_address_1': order.address_1,
                'default_address_2': order.address_2,
            }
            customer_profile_form = CustomerProfileForm(
                profile_data, instance=profile)
            if customer_profile_form.is_valid():
                customer_profile_form.save()

            messages.success(
                request, 'Your details have been saved to your account.')

    # # Send success message to user
    messages.success(request, f'Order successfully sent to the restaurant! \
        Your order number is {order_number}. A confirmation email will be sent to {order.email}')

    # Remove the bag from the session
    if 'bag' in request.session:
        del request.session['bag']
    if 'restaurant' in request.session:
        del request.session['restaurant']
    if 'delivery_time' in request.session:
        del request.session['delivery_time']
    if 'save_info' in request.session:
        del request.session['save_info']

    context = {
        'order': order,
        'dynamic_navbar': True,
    }
    return render(request, 'checkout/order_confirmation.html', context)


# Post additional order data (data that doesn't fit within Stripe's confirmCardPayment's 'payment_method') to the payment intent via the intent's metadata.
# This allows the order instance in the db to be created when Stripe sends back the payment succeeded webhook to confirm that everything has gone smoothly.
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
        messages.error(
            request, 'Sorry, your payment cannot be processed right now. Please try again later.', status=400)
        return HttpResponse(content=e, status=400)
