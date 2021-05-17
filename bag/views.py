import json
from django.contrib import messages
from django.urls.base import reverse
from django.shortcuts import get_object_or_404, redirect, render
from django.http.response import HttpResponse
from checkout.models import Order
from restaurants.models import FoodItem, MenuSection, Restaurant


def view_bag(request):
    bag = request.session.get('bag', {})
    context = {
        'bag': bag,
    }
    return render(request, 'bag/bag.html', context)


def add_to_bag(request):
    # Get data
    food_id = request.POST.get('this_food')
    food = get_object_or_404(FoodItem, pk=food_id)
    menu_section = get_object_or_404(MenuSection, fooditem__name=food.name)
    restaurant = get_object_or_404(Restaurant, menusection__name=menu_section.name)
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    additional_details = request.POST.get('additional-details')
    bag = request.session.get('bag', {})
    bag_keys = list(bag.keys())

    # If bag has something in it
    if bag_keys:
        # If food from this restaurant is already in the bag
        if bag_keys[0] == restaurant.name:
            # If the same food exists in the bag, update quantity
            if food_id in list(bag[restaurant.name].keys()):
                bag[restaurant.name][food_id]['quantity'] += quantity
                # If food being added has additional details
                if additional_details:
                    # If same food in bag already has additional details, add comma to separate
                    if bag[restaurant.name][food_id]['additional_details']:
                        bag[restaurant.name][food_id]['additional_details'] += ', ' + additional_details
                    # Else add additional details
                    else:
                        bag[restaurant.name][food_id]['additional_details'] += additional_details
                messages.success(request, f'Updated quantity of {food.friendly_name} to {bag[restaurant.name][food_id]["quantity"]}')
            # Else add food and set quantity
            else:
                bag[restaurant.name][food_id] = {'quantity': quantity, 'additional_details': additional_details}
                messages.success(request, f'Added {bag[restaurant.name][food_id]["quantity"]} {food.friendly_name} to your cart')
        # Else if there is food from another restaurant in the bag, throw error (elif used for extra verification)
        elif bag_keys[0] != restaurant.name:
            messages.error(request, 'There is already food from another restaurant in your cart.')
    # Else add food to bag
    else:
        bag[restaurant.name] = {food_id: {'quantity': quantity, 'additional_details': additional_details}}
        # If quantity being added is more than 1, say quantity in toast
        if quantity > 1:
            messages.success(request, f'Added {quantity} of {food.friendly_name} to your cart')
        else:
            messages.success(request, f'Added {food.friendly_name} to your cart')
        
    
    request.session['bag'] = bag

    return redirect(redirect_url)


def remove_from_bag(request, food_id):
    try:
        bag = request.session.get('bag', {})
        food = get_object_or_404(FoodItem, pk=food_id)
        menu_section = get_object_or_404(MenuSection, fooditem__name=food.name)
        restaurant = get_object_or_404(Restaurant, menusection__name=menu_section.name)
        bag[restaurant.name].pop(food_id)
        request.session['bag'] = bag
        if not bag[restaurant.name]:
            del request.session['bag']
        messages.info(request, f'{food.friendly_name} has been removed from your order')
        return redirect(reverse('view_bag'))
        
    except Exception as e:
        return HttpResponse(status=500)


def order_again(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)
    bag = json.loads(order.original_bag)
    bag_keys = list(bag.keys())

    if 'bag' in request.session:
        del request.session['bag']
    
    for item in order.lineitems.all():
        # Get data
        food_object = item.food_item
        food_id = food_object.id
        menu_section = get_object_or_404(MenuSection, fooditem__name=food_object.name)
        restaurant = get_object_or_404(Restaurant, menusection__name=menu_section.name)
        restaurant_name = restaurant.name
        quantity = int(item.quantity)
        additional_details = item.additional_details

        # If bag has something in it
        if bag_keys:
            # If food from this restaurant is already in the bag
            if bag_keys[0] == restaurant_name:
                # If the same food exists in the bag, update quantity
                if food_id in list(bag[restaurant_name].keys()):
                    bag[restaurant_name][food_id]['quantity'] += quantity
                    # If food being added has additional details
                    if additional_details:
                        # If same food in bag already has additional details, add comma to separate
                        if bag[restaurant_name][food_id]['additional_details']:
                            bag[restaurant_name][food_id]['additional_details'] += ', ' + additional_details
                        # Else add additional details
                        else:
                            bag[restaurant_name][food_id]['additional_details'] += additional_details
                    messages.success(request, f'Updated quantity of {food_object.friendly_name} to {bag[restaurant_name][food_id]["quantity"]}')
                # Else add food and set quantity
                else:
                    bag[restaurant_name][food_id] = {'quantity': quantity, 'additional_details': additional_details}
                    messages.success(request, f'Added {bag[restaurant_name][food_id]["quantity"]} {food_object.friendly_name} to your cart')
            # Else if there is food from another restaurant in the bag, throw error (elif used for extra verification)
            elif bag[0] != restaurant_name:
                messages.error(request, 'There is already food from another restaurant in your cart.')
        # Else add food to bag
        else:
            bag[restaurant_name] = {food_id: {'quantity': quantity, 'additional_details': additional_details}}
            # If quantity being added is more than 1, say quantity in toast
            if quantity > 1:
                messages.success(request, f'Added {quantity} of {food_object.friendly_name} to your cart')
            else:
                messages.success(request, f'Added {food_object.friendly_name} to your cart')
            

        request.session['bag'] = bag

        return redirect('/bag')
