from django.http import response
from django.shortcuts import get_object_or_404, render
from .models import FoodItem, Restaurant, MenuSection

# Create your views here.

def all_restaurants(request):
    restaurants = Restaurant.objects.all()
    context =  {
        'restaurants': restaurants,
    }
    return render(request, 'restaurants/restaurants.html', context)


def restaurant_menu(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
    menu_sections = MenuSection.objects.all().filter(restaurant=restaurant)

    food_items = []
    for section in menu_sections:
        food_items += FoodItem.objects.all().filter(menu_section=section)

    context = {
        'restaurant': restaurant,
        'menu_sections': menu_sections,
        'food_items': food_items,
    }
    return render(request, 'restaurants/restaurant_menu.html', context)
