from django.http import response
from django.shortcuts import get_object_or_404, render
from .models import Restaurant

# Create your views here.

def all_restaurants(request):
    restaurants = Restaurant.objects.all()
    context =  {
        'restaurants': restaurants,
    }
    return render(request, 'restaurants/restaurants.html', context)


def restaurant_menu(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
    print(restaurant)
    context = {
        'restaurant': restaurant,
    }
    return render(request, 'restaurants/restaurant_menu.html', context)
