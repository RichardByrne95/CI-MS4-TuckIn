import os
from restaurants.views import FoodItem
from restaurants.models import Restaurant
from django.shortcuts import get_object_or_404


def bag_contents(request):
    order_total = 0
    forloop_count = 0
    food_item_count = 0
    bag_contents = []
    current_restaurant = None
    bag = request.session.get('bag', {})
    contact_email = os.getenv('EMAIL_HOST_USER')
    maps_address = request.session.get('maps_address', None)
    short_maps_address = request.session.get('short_maps_address', None)
    
    # Add restuarant name to session
    current_restaurant = get_object_or_404(
        Restaurant, name=list(bag)[0]) if bag else None
    request.session['restaurant'] = current_restaurant.name if bag else ''

    # Get delivery cost from current restaurant
    delivery_cost = current_restaurant.delivery_cost if bag else 0
    
    for restaurant, food_items in bag.items():
        list_of_food_keys_in_bag = list(food_items.keys())

        for food_item in bag[restaurant]:
            food_id = list_of_food_keys_in_bag[forloop_count]
            food_object = get_object_or_404(FoodItem, pk=food_id)
            quantity = bag[restaurant][food_id]['quantity']
            additional_details = bag[restaurant][food_id]['additional_details']
            order_total += quantity * food_object.price
            forloop_count += 1
            bag_contents.append({
                'food_id': food_id,
                'food': food_object,
                'quantity': quantity,
                'additional_details': additional_details,
            })

    # Get food item count
    for food in bag_contents:
        food_item_count += food['quantity']

    # food_item_count = len(bag_contents) if bag_contents else 0
    grand_total = order_total + delivery_cost

    context = {
        'current_restaurant': current_restaurant,
        'bag_contents': bag_contents,
        'food_item_count': food_item_count,
        'order_total': order_total,
        'delivery_cost': delivery_cost,
        'grand_total': grand_total,
        'maps_address': maps_address,
        'short_maps_address': short_maps_address,
        'contact_email': contact_email,
    }

    return context
