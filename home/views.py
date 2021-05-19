from django.shortcuts import render
from restaurants.models import Cuisine


def home(request):
    cuisines = Cuisine.objects.all()
    context = {
        'cuisines': cuisines,
        'dynamic_navbar': True,
    }
    return render(request, 'home/index.html', context)
