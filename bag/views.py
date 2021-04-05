from restaurants.views import restaurant_menu
from restaurants.models import FoodItem, MenuSection, Restaurant
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.contrib import messages


def view_bag(request):
    return render(request, 'bag/bag.html')


def add_to_bag(request):
    food_id = request.POST.get('this_food')
    food = get_object_or_404(FoodItem, pk=food_id)
    print(food.menu_section)
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    bag = request.session.get('bag', {})

    if food_id in list(bag.keys()):
        bag[food_id] += quantity
        messages.success(request, f'Updated {food.friendly_name} quantity to {bag[food_id]}')
    else:
        bag[food_id] = quantity
        messages.success(request, f'Added {food.friendly_name} to your basket')
    request.session['bag'] = bag

    return redirect(redirect_url)
