from django.shortcuts import render
from restaurants.models import Cuisine

# Create your views here.
def list_your_restaurant(request):
    cuisines = Cuisine.objects.all()
    print(cuisines)
    context = {
        'cuisines': cuisines,
    }
    return render(request, 'footer_links/list_your_restaurant.html', context)
