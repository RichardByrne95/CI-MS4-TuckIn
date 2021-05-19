from restaurants.models import Cuisine
from django.shortcuts import render

# Create your views here.
def home(request):
    cuisines = Cuisine.objects.all()
    context = {
        'cuisines': cuisines,
        'dynamic_navbar': True,
    }
    return render(request, 'home/index.html', context)
