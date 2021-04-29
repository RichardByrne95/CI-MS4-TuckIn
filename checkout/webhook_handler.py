from django.http import HttpResponse

# Class to handle stripe webhooks
class StripeWH_Handler:
    # Add current request object as attribute of class
    def __init__(self, request):
        self.request = request

    # Stripe Webhook event handler
    def handle_event(self, event):
        return HttpResponse(
            content=f'Webhook received: {event[type]}',
            status=200,
        )
