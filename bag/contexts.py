from restaurants.models import Restaurant
from django.shortcuts import get_object_or_404
from restaurants.views import FoodItem


def bag_contents(request):
    current_restaurant = None
    bag_contents = []
    total = 0
    food_item_count = 0

    bag = request.session.get('bag', {})
    count = 0
    for restaurant, food_item in bag.items():
        food_item_list = list(food_item.keys())
        food_id = food_item_list[count]
        food_object = get_object_or_404(FoodItem, pk=food_id)
        
        count +=1

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
