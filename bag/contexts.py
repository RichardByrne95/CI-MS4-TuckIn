from restaurants.models import Restaurant
from django.shortcuts import get_object_or_404
from restaurants.views import FoodItem


def bag_contents(request):
    current_restaurant = None
    bag_contents = []
    food_item_count = 0
    forloop_count = 0
    order_total = 0
    bag = request.session.get('bag', {})

    for restaurant, food_items in bag.items():
        current_restaurant = get_object_or_404(Restaurant, name=restaurant)
        list_of_food_keys_in_bag = list(food_items.keys())
        delivery_cost = current_restaurant.delivery_cost

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
    
    food_item_count = len(bag_contents)
    grand_total = order_total + delivery_cost
    
    context = {
        'current_restaurant': current_restaurant,
        'bag_contents': bag_contents,
        'food_item_count': food_item_count,
        'order_total': order_total,
        'delivery_cost': delivery_cost,
        'grand_total': grand_total,
    }

    return context
