from restaurants.models import Restaurant
from django.shortcuts import render
from restaurants.models import Cuisine

# Create your views here.
def home(request):
    cuisines = Cuisine.objects.all()
    context = {
        'cuisines': cuisines,
    }
    return render(request, 'home/index.html', context)
