# Referenced Boutique Ado
def bag_contents(request):
    current_restaurant = None
    bag_contents = []
    total = 0
    food_item_count = 0
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