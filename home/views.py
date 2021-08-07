from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import render
from restaurants.models import Cuisine


def home(request):
    try:
        cuisines = Cuisine.objects.all()
        context = {
            'cuisines': cuisines,
            'dynamic_navbar': True,
        }
        return render(request, 'home/index.html', context)
    except Exception as e:
        return HttpResponse(request, 'Error loading homepage. Please contact support@tuckin.com for assistance.')
