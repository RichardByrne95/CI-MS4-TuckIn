from home.views import home
from django.db.models import Q
from django.contrib import messages
from django.urls.base import reverse
from .models import FoodItem, Restaurant, MenuSection, Cuisine
from django.shortcuts import get_object_or_404, redirect, render


def all_restaurants(request):
    all_cuisines = None
    sortkey = None
    refine_text = None
    direction = None
    query_search = None
    cuisine = None

    # Get restaurants
    restaurants = Restaurant.objects.all()
    open_restaurants = [
        restaurant.name for restaurant in restaurants if restaurant.is_open_now()]
    open_restaurants = restaurants.filter(name__in=open_restaurants)
    closed_restaurants = [
        restaurant for restaurant in restaurants if not restaurant.is_open_now()]
    closed_restaurants = restaurants.filter(name__in=closed_restaurants)

    #  Handle inputting/changing delivery address
    if request.method == 'POST':
        try:
            maps_address = request.POST['maps_address']

            # Create address without city and country
            short_maps_address_list = maps_address.split(',')
            short_maps_address = f'{short_maps_address_list[0]}, {short_maps_address_list[1]}'
            # Store in session
            request.session['maps_address'] = maps_address
            request.session['short_maps_address'] = short_maps_address
        
        except Exception:
            messages.error(request, 'Address could not be found. Please ensure the address is valid, uses commas, is within Dublin, Ireland and is foramtted correctly.')
            return redirect(reverse(home))

    # Sorting (referenced Boutique Ado)
    if request.method == 'GET':
        # Search Request (referenced Boutique Ado)
        if 'q' in request.GET:
            redirect_url = request.GET['redirect_url']
            query_search = request.GET['q']
            if not query_search:
                messages.error(
                    request, "You didn't enter any search criteria!")
                return redirect(redirect_url)
            # Referenced book for advanced queries https://books.agiliq.com/projects/django-orm-cookbook/en/latest/query.html
            queries = Q(name__icontains=query_search) | Q(friendly_name__icontains=query_search) | Q(
                description__icontains=query_search) | Q(cuisine__name__icontains=query_search) | Q(
                    menusection__name__icontains=query_search) | Q(
                        menusection__friendly_name__icontains=query_search) | Q(
                        menusection__fooditem__name__icontains=query_search) | Q(
                            menusection__fooditem__friendly_name__icontains=query_search) | Q(
                                menusection__fooditem__description__icontains=query_search)
            restaurants = restaurants.filter(queries).distinct()
            # Filter queried restaurants by whether they're open or closed
            open_restaurants = [
                restaurant.name for restaurant in restaurants if restaurant.is_open_now()]
            open_restaurants = restaurants.filter(name__in=open_restaurants)
            closed_restaurants = [
                restaurant for restaurant in restaurants if not restaurant.is_open_now()]
            closed_restaurants = restaurants.filter(name__in=closed_restaurants)
            
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            if sortkey == 'rating_high':
                sortkey = 'rating'
                refine_text = 'Rating'
            elif sortkey == 'delivery_cost':
                refine_text = 'Delivery'

            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'

            restaurants = restaurants.order_by(sortkey)
            open_restaurants = open_restaurants.order_by(sortkey)
            closed_restaurants = closed_restaurants.order_by(sortkey)

        # Sorting by Cuisine (referenced Boutique Ado)
        if 'cuisine' in request.GET:
            cuisine = request.GET['cuisine']
            restaurants = restaurants.filter(
                Q(cuisine__name__icontains=cuisine))
            open_restaurants = open_restaurants.filter(
                Q(cuisine__name__icontains=cuisine))
            closed_restaurants = closed_restaurants.filter(
                Q(cuisine__name__icontains=cuisine))
            # Turns list of strings from url to cuisine object for use in template
            cuisine = Cuisine.objects.filter(Q(name=cuisine))[0]

    current_sorting = f'{sortkey}_{direction}'
    all_cuisines = Cuisine.objects.all()

    context = {
        'restaurants': restaurants,
        'open_restaurants': open_restaurants,
        'closed_restaurants': closed_restaurants,
        'refine_text': refine_text,
        'search_term': query_search,
        'all_cuisines': all_cuisines,
        'current_cuisine': cuisine,
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
        'dynamic_navbar': True,
    }
    return render(request, 'restaurants/restaurant_menu.html', context)
