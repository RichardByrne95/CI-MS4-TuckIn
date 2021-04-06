from django.shortcuts import get_object_or_404
from restaurants.views import FoodItem


def bag_contents(request):
    current_restaurant = None
    bag_contents = []
    total = 0
    food_item_count = 0

    bag = request.session.get('bag', {})
    for food_id, quantity in bag.items():
        food = get_object_or_404(FoodItem, pk=food_id)
        total += quantity * food.price
        food_item_count += quantity
        bag_contents.append({
            'food_id': food_id,
            'quantity': quantity,
            'food': food,
        })

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
