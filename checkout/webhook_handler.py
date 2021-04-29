import json
from django.contrib import messages
from stripe.api_resources import payment_intent
from django.urls.base import reverse
from django.shortcuts import get_object_or_404, redirect
from restaurants.models import FoodItem
from django.http import HttpResponse
from checkout.models import Order, OrderLineItem


# Class to handle stripe webhooks
class StripeWH_Handler:
    # Add current request object as attribute of class
    def __init__(self, request):
        self.request = request

    # Unhandled webhook event handler
    def handle_event(self, event):
        return HttpResponse(
            content=f'Webhook received: {event[type]}',
            status=200,
        )

    # Payment Intent Succeeded webhook event handler
    def handle_payment_intent_succeeded(self, event):
        # Get order data from payment intent
        intent = event.data.object
        payment_intent_id = intent.id
        bag = intent.metadata.bag
        save_info = intent.metadata.save_info
        billing_details = intent.charges.data[0].billing_details
        shipping_details = intent.shipping
        grand_total = round(intent.data.charges[0].amount / 100, 2)

        # Replace empty strings with Null for db compatibility
        for field, value in shipping_details.address.items():
            if value == "":
                shipping_details.address[field] = None

        order_exists = False

        try:
            # Check if order already exists in database
            order = get_object_or_404(Order,
                full_name__iexact=shipping_details.name,
                address_1__iexact=shipping_details.line1,
                address_2__iexact=shipping_details.line2,
                city__iexact=shipping_details.city,
                postcode__iexact=shipping_details.postcode,
                email__iexact=shipping_details.email,
                phone_number__iexact=shipping_details.phone_number,
                grand_total=grand_total,
            )
            order_exists = True
            return HttpResponse(
                content=f'Webhook received: {event[type]} | SUCCESS: Verified order already in database',
                status=200,
            )
        except Order.DoesNotExist:
            try:
                # Create order
                order = Order.objects.create(Order,
                    full_name=shipping_details.name,
                    address_1=shipping_details.line1,
                    address_2=shipping_details.line2,
                    city=shipping_details.city,
                    postcode=shipping_details.postcode,
                    email=shipping_details.email,
                    phone_number=shipping_details.phone_number,
                    grand_total=grand_total,
                )
                # Create line items (taken from contexts.py)
                bag = json.loads(bag)
                forloop_count = 0
                for restaurant, food_items in bag.items():
                    list_of_food_keys_in_bag = list(food_items.keys())
                    food_id = list_of_food_keys_in_bag[forloop_count]
                    food_object = get_object_or_404(FoodItem, pk=food_id)
                    quantity = bag[restaurant][food_id]['quantity']
                    for food in bag[restaurant]:
                        order_line_item = OrderLineItem(
                            order=order,
                            food_item=food_object,
                            quantity=bag[restaurant][food_id]['quantity'],
                        )
                        order_line_item.save()
                        forloop_count += 1
            except Exception as e:
                if order:
                    order.delete()
                return HttpResponse(content=f'Webhook received: {event[type]} | ERROR: {e}', status=500)
                
        return HttpResponse(
            content=f'Webhook received: {event[type]}',
            status=200,
        )

    # Payment Intent Payment Failed webhook event handler
    def handle_payment_intent_payment_failed(self, event):
        return HttpResponse(
            content=f'Payment Failed Webhook received: {event[type]}',
            status=200,
        )
