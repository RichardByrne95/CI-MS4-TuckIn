import json
import time
from django.conf import settings
from django.http import HttpResponse
from django.core.mail import send_mail
from restaurants.models import FoodItem
from django.shortcuts import get_object_or_404
from checkout.models import Order, OrderLineItem
from django.template.loader import render_to_string


# Class to handle the different stripe webhooks
class StripeWH_Handler:
    # Add current request object as attribute of class
    def __init__(self, request):
        self.request = request

    # Send order confirmation email
    def _send_confirmation_email(self, order):
        customer_email = order.email
        subject = render_to_string(
            'checkout/confirmation_emails/confirmation_email_subject.txt',
            {'order': order}
        )
        body = render_to_string(
            'checkout/confirmation_emails/confirmation_email_body.txt',
            {'order': order, 'contact_email': settings.DEFAULT_FROM_EMAIL}
        )

        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [customer_email]
        )

    # Unhandled webhook event handler
    def handle_event(self, event):
        return HttpResponse(
            content='Webhook received: {}'.format(event.type),
            status=200,
        )

    # Payment Intent Succeeded webhook event handler
    def handle_payment_intent_succeeded(self, event):
        # Get order data from payment intent
        intent = event.data.object
        payment_intent_id = intent.id
        bag = json.loads(
            intent.metadata.bag) if intent.metadata and intent.metadata.bag else None
        billing_details = intent.charges.data[0].billing_details if intent.charges.data[0].billing_details else None
        shipping_details = intent.shipping if intent.shipping else None
        grand_total = round(intent.charges.data[0].amount / 100, 2)

        # If no bag in metadata
        if not bag:
            return HttpResponse(
                content='No bag or items associated with this order | {}'.format(
                    intent),
                status=400
            )

        # If no billing details
        if not billing_details:
            return HttpResponse(
                content='No billing details associated with this order | {}'.format(
                    intent),
                status=400
            )

        # If no shipping details
        if not shipping_details:
            return HttpResponse(
                content='No shipping details associated with this order | {}'.format(
                    intent),
                status=400
            )

        # Replace empty strings with Null for db compatibility
        for field, value in shipping_details.address.items():
            if value == '':
                shipping_details.address[field] = None

        order_exists = False
        attempt = 1

        # Attempt to find order in database 5 times
        while attempt <= 5:
            # Check if order already exists in database
            try:
                order = get_object_or_404(Order,
                                          stripe_payment_id=payment_intent_id,
                                          )
                order_exists = True
                break
            # Increase attempt, sleep 1 second
            except Order.DoesNotExist:
                attempt += 1
                time.sleep(1)

        if order_exists:
            # Send confirmation email
            self._send_confirmation_email(order)
            return HttpResponse(
                content='Webhook received: {} | SUCCESS: Verified order already in database'.format(
                    event.type),
                status=200,
            )
        else:
            order = None
            try:
                # Create order
                order = Order.objects.create(Order,
                                             full_name=shipping_details.name,
                                             address_1=shipping_details.line1,
                                             address_2=shipping_details.line2,
                                             city=shipping_details.city,
                                             postcode=shipping_details.postcode,
                                             email=billing_details.email,
                                             phone_number=billing_details.phone_number,
                                             grand_total=grand_total,
                                             original_bag=bag,
                                             stripe_payment_id=payment_intent_id,
                                             )
                # Create line items (taken from contexts.py)
                if bag:
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
                else:
                    return HttpResponse(
                        content='Bag does not exist',
                        status=400
                    )
            except Exception as e:
                if order:
                    order.delete()
                return HttpResponse(
                    content='Webhook received: {} | ERROR: {}'.format(
                        event.type, e),
                    status=500
                )

        # Send confirmation email
        self._send_confirmation_email(order)
        return HttpResponse(
            content='Webhook received: {} | SUCCESS: Created order via Webhook handler'.format(
                event.type),
            status=200,
        )

    # Payment Intent Payment Failed webhook event handler
    def handle_payment_intent_payment_failed(self, event):
        return HttpResponse(
            content='Payment Failed Webhook received: {}'.format(event.type),
            status=200,
        )
