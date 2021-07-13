from django.shortcuts import render
from restaurants.models import Cuisine
from django.views.decorators.clickjacking import xframe_options_exempt


@xframe_options_exempt
def home(request):
    cuisines = Cuisine.objects.all()
    context = {
        'cuisines': cuisines,
        'dynamic_navbar': True,
    }
    return render(request, 'home/index.html', context)
