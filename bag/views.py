from restaurants.views import restaurant_menu
from restaurants.models import FoodItem, MenuSection, Restaurant
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.contrib import messages


def view_bag(request):
    bag = request.session.get('bag', {})
    context = {
        'bag': bag,
    }
    return render(request, 'bag/bag.html')


def add_to_bag(request):
    food_id = request.POST.get('this_food')
    food = get_object_or_404(FoodItem, pk=food_id)
    menu_section = MenuSection.objects.get(fooditem__name=food.name)
    restaurant = Restaurant.objects.get(menusection__name=menu_section.name)
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    additional_details = request.POST.get('additional-details')
    bag = request.session.get('bag', {})

    # If food from this restaurant is already in the bag
    bag_keys = list(bag.keys())
    # If bag has something in it
    if bag_keys:
        # If the food being added is from the restaurant that already has food in the bag
        if bag_keys[0] == restaurant.name:
            # If the same food exists in the bag, change quantity
            if food_id in list(bag[restaurant.name].keys()):
                bag[restaurant.name][food_id]['quantity'] += quantity
                bag[restaurant.name][food_id]['additional_details'] += ", " + additional_details
            # Else add food and set quantity
            else:
                bag[restaurant.name][food_id] = {"quantity": quantity, "additional_details": additional_details}
        # Else if there is food from another restaurant in the bag
        elif bag_keys[0] != restaurant.name:
            # Throw error
            print("There is already food from another restaurant here.")
            request.session['bag'] = bag
            return redirect(redirect_url)
    # Else add food to bag
    else:
        bag[restaurant.name] = {food_id: {"quantity": quantity, "additional_details": additional_details}}

    request.session['bag'] = bag
    messages.warning(request, f"Added {food.friendly_name} to your cart")

    return redirect(redirect_url)
