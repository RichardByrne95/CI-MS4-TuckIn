from django.http import HttpResponse

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
        return HttpResponse(
            content=f'Webhook received: {event[type]}',
            status=200,
        )

    # Payment Intent Payment Failed webhook event handler
    def handle_payment_intent_payment_failed(self, event):
        return HttpResponse(
            content=f'Webhook received: {event[type]}',
            status=200,
        )
