from django.db import models
from django.db.models.deletion import CASCADE, SET_NULL

class Cuisine(models.Model):
    name = models.CharField(max_length=254)

    def __str__(self):
        return self.name

class Restaurant(models.Model):
    cuisine = models.ForeignKey('Cuisine', null=True, blank=True, on_delete=SET_NULL)
    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, default="Please set friendly name")
    description = models.TextField()
    rating = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    logo = models.ImageField(null=True, blank=True)
    cover_image = models.ImageField(null=True, blank=True)
    address_1 = models.CharField(max_length=254, default="Please enter address")
    address_2 = models.CharField(max_length=254, default="Please enter address", null=True, blank=True)
    post_code = models.CharField(max_length=254, default="Please enter post code")
    delivery_cost = models.DecimalField(max_digits=4, decimal_places=2, default="0.00")

    def __str__(self):
        return self.name
    
    def get_friendly_name(self):
        return self.friendly_name

class MenuSection(models.Model):
    restaurant = models.ForeignKey('Restaurant', on_delete=CASCADE)
    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, default="Please set friendly name")

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name

class FoodItem(models.Model):
    menu_section = models.ForeignKey('MenuSection', on_delete=CASCADE)
    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(null=True, blank=True)
    is_vegetarian = models.BooleanField(null=True, blank=True)
    is_vegan = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return self.name
    
    def get_friendly_name(self):
        return self.friendly_name
