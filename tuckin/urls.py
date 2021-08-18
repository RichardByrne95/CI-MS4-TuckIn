import debug_toolbar
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('__debug__/', include(debug_toolbar.urls)),
    path('', include('home.urls')),
    path('accounts/', include('allauth.urls')),
    path('restaurants/', include('restaurants.urls')),
    path('profiles/', include('profiles.urls')),
    path('links/', include('footer_links.urls')),
    path('bag/', include('bag.urls')),
    path('checkout/', include('checkout.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'tuckin.views.handler404'
