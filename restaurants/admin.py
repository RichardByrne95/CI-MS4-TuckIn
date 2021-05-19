from django.contrib import admin
from .models import OpeningHours, Restaurant, Cuisine, MenuSection, FoodItem


class CuisineAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'icon_html',
    )

    ordering = ('name',)


class RestaurantsAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
        'cuisine',
        'rating',
        'delivery_cost',
    )

    ordering = ('name',)


class OpeningHoursAdmin(admin.ModelAdmin):
    list_display = (
        'restaurant',
        'weekday',
        'from_hour',
        'to_hour',
    )

    ordering = ('restaurant', 'weekday',)


class MenuSectionAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'friendly_name',
        'restaurant',
    )

    ordering = ('name',)


class FoodItemAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'friendly_name',
        'menu_section',
        'description',
        'price',
        'is_vegetarian',
        'is_vegan',
    )

    ordering = ('name',)


admin.site.register(Restaurant, RestaurantsAdmin)
admin.site.register(OpeningHours, OpeningHoursAdmin)
admin.site.register(Cuisine, CuisineAdmin)
admin.site.register(MenuSection, MenuSectionAdmin)
admin.site.register(FoodItem, FoodItemAdmin)
