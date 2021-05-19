from django.shortcuts import render
from restaurants.models import Cuisine

# Create your views here.
def list_your_restaurant(request):
    cuisines = Cuisine.objects.all()
    context = {
        'cuisines': cuisines,
        'dynamic_navbar': True,
    }
    return render(request, 'footer_links/list_your_restaurant.html', context)
