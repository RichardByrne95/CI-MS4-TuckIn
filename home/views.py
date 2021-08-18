from django.shortcuts import render
from restaurants.models import Cuisine
from django.http.response import Http404, HttpResponse


def home(request):
    try:
        cuisines = Cuisine.objects.all()
        context = {
            'cuisines': cuisines,
            'dynamic_navbar': True,
        }
        return render(request, 'home/index.html', context)
    except Exception:
        raise Http404(request, 'Error loading homepage. Please contact support@tuckin.com for assistance.')
