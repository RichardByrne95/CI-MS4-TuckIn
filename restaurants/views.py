from django.http import response
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.contrib import messages
from django.db.models import Q
from .models import FoodItem, Restaurant, MenuSection


def all_restaurants(request):
    restaurants = Restaurant.objects.all()
    query = None

    # Search Request (referenced Boutique Ado)
    if request.GET:
        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(
                    request, "You didn't enter any search criteria!")
                return redirect(reverse('restaurants'))
            # Referenced book for advanced queries https://books.agiliq.com/projects/django-orm-cookbook/en/latest/query.html
            queries = Q(name__icontains=query) | Q(friendly_name__icontains=query) | Q(
                description__icontains=query) | Q(cuisine__name__icontains=query) | Q(
                    menusection__name__icontains=query) | Q(
                        menusection__friendly_name__icontains=query) | Q(
                        menusection__fooditem__name__icontains=query) | Q(
                            menusection__fooditem__friendly_name__icontains=query) | Q(
                                menusection__fooditem__description__icontains=query)
            restaurants = restaurants.filter(queries).distinct()

    context =  {
        'restaurants': restaurants,
        'search_term': query,
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
