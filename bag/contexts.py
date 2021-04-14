from django.shortcuts import get_object_or_404
from restaurants.models import Restaurant
from restaurants.views import FoodItem


def bag_contents(request):
    current_restaurant = None
    bag_contents = []
    list_of_food_keys_in_bag = []
    total = 0
    food_item_count = 0

    bag = request.session.get('bag', {})
    count = 0
    for restaurant, food_items in bag.items():
        current_restaurant = restaurant
        for food_item in bag[restaurant]:
            list_of_food_keys_in_bag = list(food_items.keys())
            food_id = list_of_food_keys_in_bag[count]
            food_object = get_object_or_404(FoodItem, pk=food_id)
            quantity = bag[restaurant][food_id]['quantity']
            additional_details = bag[restaurant][food_id]['additional_details']
            total += quantity * food_object.price
            count +=1
            bag_contents.append({
                'food_id': food_id,
                'food': food_object,
                'quantity': quantity,
                'additional_details': additional_details,
            })

    food_item_count = len(bag_contents)
    delivery = 0
    grand_total = total + delivery

    context = {
        'current_restaurant': current_restaurant,
        'bag_contents': bag_contents,
        'total': total,
        'food_item_count': food_item_count,
        'delivery': delivery,
        'grand_total': grand_total,
    }

    return context
