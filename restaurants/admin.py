from django.contrib import admin
from .models import Restaurant, Cuisine, MenuSection, FoodItem

class RestaurantsAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
        'cuisine',
        'rating',
        'delivery_charge',
    )

    ordering = ('name',)

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
admin.site.register(Cuisine)
admin.site.register(MenuSection, MenuSectionAdmin)
admin.site.register(FoodItem, FoodItemAdmin)