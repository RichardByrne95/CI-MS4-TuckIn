import stripe
from django.conf import settings
from django.http import HttpResponse
from stripe.api_resources import payment_intent
from .webhook_handler import StripeWH_Handler
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

# Referenced https://stripe.com/docs/webhooks/build#example-code
@require_POST  # Only react to post requests, reject GET requests
@csrf_exempt  # Stripe doesn't send CSRF tokens
def webhook(request):
    # Set variables
    wh_secret = settings.STRIPE_WH_SECRET
    stripe.api_key = settings.STRIPE_SECRET_KEY
    stripe.api_version = '2020-08-27'
    signature = request.headers.get('stripe-signature')

    # Get webhook data and verify its signature
    payload = request.body
    event = None

    try:
        # Get webhook from Stripe
        event = stripe.Webhook.construct_event(
            payload=payload,
            sig_header=signature,
            secret=wh_secret,
            api_key=stripe.api_key
        )
    # Invalid payload exception handler
    except ValueError as e:
        return HttpResponse(content=e, status=400)
    # Invalid Signature exception handler
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(content=e, status=400)
    # Generic exception handler
    except Exception as e:
        return HttpResponse(content=e, status=400)

    # Setup webhook handler
    handler = StripeWH_Handler(request)

    # Map webhook events to relevant handler functions
    event_map = {
        'payment_intent.succeeded': handler.handle_payment_intent_succeeded,
        'payment_intent.payment_failed': handler.handle_payment_intent_payment_failed,
    }

    # Get webhook type from Stripe
    event_type = event['type']
    # Use generic handler if not available
    event_handler = event_map.get(event_type, handler.handle_event)

    # Call the event handler with the event
    response = event_handler(event)

    return HttpResponse(content=event.data.object, status=200)
