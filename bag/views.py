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
    menu_section = MenuSection.objects.all().filter(name=food.menu_section)
    restaurant = Restaurant.objects.get(menusection__in=menu_section)
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    bag = request.session.get('bag', {})

    if food_id in list(bag.keys()):
        bag[food_id] += quantity
    else:
        bag[food_id] = quantity
    request.session['bag'] = bag

    return redirect(redirect_url)
