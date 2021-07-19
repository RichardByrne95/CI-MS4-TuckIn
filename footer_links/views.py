from django.shortcuts import render
from django.contrib import messages
from restaurants.models import Cuisine


def list_your_restaurant(request):
    if request.method == 'POST':
        messages.success(
            request, 'Thank you for your interest in becoming a part of the TuckIn family. A member of our team will be in touch shortly.')

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


def help(request):
    context = {
        'dynamic_navbar': True,
    }
    return render(request, 'footer_links/help.html', context)
