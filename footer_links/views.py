from django.shortcuts import render
from restaurants.models import Cuisine


def list_your_restaurant(request):
    cuisines = Cuisine.objects.all()
    context = {
        'cuisines': cuisines,
        'dynamic_navbar': True,
    }
    return render(request, 'footer_links/list_your_restaurant.html', context)


def cookies_policy(request):
    context = {
        'dynamic_navbar': True,
    }
    return render(request, 'footer_links/cookies_policy.html', context)


def privacy_policy(request):
    context = {
        'dynamic_navbar': True,
    }
    return render(request, 'footer_links/privacy_policy.html', context)
