import datetime
from django.db import models
from django.db.models.deletion import CASCADE, SET_NULL

# Cuisine
class Cuisine(models.Model):
    name = models.CharField(max_length=254)
    icon_html = models.TextField(max_length=254, default="Please enter icon html")

    def __str__(self):
        return self.name

# Restaurant
class Restaurant(models.Model):
    cuisine = models.ForeignKey('Cuisine', null=True, blank=True, on_delete=SET_NULL)
    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, default="Please set friendly name")
    description = models.TextField()
    rating = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    opening_hours = models.TextField(max_length=254, null=True, blank=True, default="Please enter opening hours")
    logo = models.ImageField(null=True, blank=True)
    cover_image = models.ImageField(null=True, blank=True)
    address_1 = models.CharField(max_length=254, default="Please enter address 1")
    address_2 = models.CharField(max_length=254, default="Please enter address 2", null=True, blank=True)
    post_code = models.CharField(max_length=254, default="Please enter post code")
    delivery_cost = models.DecimalField(max_digits=4, decimal_places=2, default="0.00")
    phone_number = models.DecimalField(max_digits=10, decimal_places=0, blank=False, null=False, default=0)

    def get_opening_hours(self):
        today = datetime.datetime.today().weekday()
        opening_hours = self.hours.all()
        todays_opening_hours = opening_hours.filter(weekday=today)
        opening_time = str(todays_opening_hours[0].from_hour)[:-3]
        closing_time = str(todays_opening_hours[0].to_hour)[:-3]
        return f'{opening_time} - {closing_time}'

    def __str__(self):
        return self.name
    
    def get_friendly_name(self):
        return self.friendly_name

# Opening Hours
# Referenced https://stackoverflow.com/questions/28450106/business-opening-hours-in-django
WEEKDAYS = [
    (1, ("Monday")),
    (2, ("Tuesday")),
    (3, ("Wednesday")),
    (4, ("Thursday")),
    (5, ("Friday")),
    (6, ("Saturday")),
    (7, ("Sunday")),
]

class OpeningHours(models.Model):
    class Meta:
        ordering = ('weekday', 'from_hour')
        unique_together = ('weekday', 'from_hour', 'to_hour')
        verbose_name_plural = 'Opening Hours'

    restaurant = models.ForeignKey("Restaurant", on_delete=CASCADE, related_name="hours")
    weekday = models.IntegerField(choices=WEEKDAYS)
    from_hour = models.TimeField()
    to_hour = models.TimeField()
    
# Menu Section
class MenuSection(models.Model):
    class Meta:
        verbose_name_plural = 'Menu Sections'
    
    restaurant = models.ForeignKey('Restaurant', on_delete=CASCADE)
    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, default="Please set friendly name")

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name

# Food Item
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
