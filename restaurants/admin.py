from django.contrib import admin
from .models import Restaurant, Cuisine, MenuSection, FoodItem

# Register your models here.
admin.site.register(Restaurant)
admin.site.register(Cuisine)
admin.site.register(MenuSection)
admin.site.register(FoodItem)