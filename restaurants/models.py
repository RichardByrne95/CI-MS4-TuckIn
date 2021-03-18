from django.db import models
from django.db.models.deletion import CASCADE, SET_NULL

class Cuisine(models.Model):
    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name

class Restaurant(models.Model):
    cuisine = models.ForeignKey('Cuisine', null=True, blank=True, on_delete=SET_NULL)
    name = models.CharField(max_length=254)
    description = models.TextField()
    rating = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    logo_url = models.URLField(max_length=1024, null=True, blank=True)
    cover_image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name

class MenuSection(models.Model):
    restaurant = models.ForeignKey('Restaurant', on_delete=CASCADE)
    name = models.CharField(max_length=254)

    def __str__(self):
        return self.name

class FoodItem(models.Model):
    menu_section = models.ForeignKey('MenuSection', on_delete=CASCADE)
    name = models.CharField(max_length=254)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(null=True, blank=True)
    is_vegetarian = models.BooleanField(null=True, blank=True)
    is_vegan = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return self.name
