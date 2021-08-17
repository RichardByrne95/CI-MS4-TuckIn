from django.shortcuts import render
from django.template import RequestContext


# Referenced https://stackoverflow.com/questions/17662928/django-creating-a-custom-500-404-error-page
def handler404(request, exception=None):
    return render(request, '404.html')


# Referenced https://stackoverflow.com/questions/17662928/django-creating-a-custom-500-404-error-page
def handler500(request, exception=None):
    return render(request, '500.html')
