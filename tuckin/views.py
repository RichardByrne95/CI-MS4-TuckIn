from django.shortcuts import render


# Referenced https://stackoverflow.com/questions/17662928/django-creating-a-custom-500-404-error-page
def handler404(request, exception=None):
    context = {
        'dynamic_navbar': True,
    }
    return render(request, '404.html', context)
