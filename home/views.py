from restaurants.models import Cuisine
from django.shortcuts import render

# Create your views here.
def home(request):
    cuisines = Cuisine.objects.all()
    context = {
        'cuisines': cuisines,
    }
    return render(request, 'home/index.html', context)
