from django.contrib import messages
from django.urls.base import reverse
from restaurants.models import Cuisine
from django.shortcuts import redirect, render


def list_your_restaurant(request):
    try:
        if request.method == 'POST':
            messages.success(
                request, 'Thank you for your interest in becoming a part of the TuckIn family. A member of our team will be in touch shortly.')

        cuisines = Cuisine.objects.all()
        context = {
            'cuisines': cuisines,
            'dynamic_navbar': True,
        }
        return render(request, 'footer_links/list_your_restaurant.html', context)

    except Exception:
        messages.error(
            request, 'Oops! Looks like an error occurred. Please try again. If this error persists, please contact us via the help section.')
        return redirect(reverse('home'))


def cookies_policy(request):
    try:
        context = {
            'dynamic_navbar': True,
        }
        return render(request, 'footer_links/cookies_policy.html', context)
    except Exception:
        messages.error(
            request, 'Oops! Looks like an error occurred. Please try again. If this error persists, please contact us via the help section.')
        return redirect(reverse('home'))


def privacy_policy(request):
    try:
        context = {
            'dynamic_navbar': True,
        }
        return render(request, 'footer_links/privacy_policy.html', context)
    except Exception:
        messages.error(
            request, 'Oops! Looks like an error occurred. Please try again. If this error persists, please contact us via the help section.')
        return redirect(reverse('home'))


def help(request):
    try:
        context = {
            'dynamic_navbar': True,
        }
        return render(request, 'footer_links/help.html', context)
    except Exception:
        messages.error(
            request, 'Oops! Looks like an error occurred. Please try again. If this error persists, please contact us via the help section.')
        return redirect(reverse('home'))
