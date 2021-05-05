import datetime
from math import ceil
from django.db import models
from django.utils.timezone import utc
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

    def get_todays_delivery_times(self):
        # Get/set variables
        today = datetime.datetime.today().weekday()
        now = datetime.datetime.today()
        opening_hours = self.hours.all()
        todays_opening_hours = opening_hours.filter(weekday=today)
        opening_time = todays_opening_hours[0].from_hour
        closing_time = todays_opening_hours[0].to_hour        
        first_delivery_time = now
        delivery_times = []

        # If closing time is midnight, replace with 23:59:59
        if datetime.time.strftime(closing_time, "%H:%M:%S") == "00:00:00":
            closing_time = datetime.time(hour=23, minute=59, second=59)


        # Convert from datetime.time to datetime.datetime object
        closing_time = datetime.datetime.strptime(
            f'{now.date()} {closing_time}', "%Y-%m-%d %H:%M:%S")

        # If restaurant is open
        if now.time() > opening_time:
            # Find next closest 15 minute interval (i.e. 15, 30, 45, 60)
            next_closest_15_minutes = ceil(now.time().minute / 15) * 15

            # If next interval is the next hour, remove minutes and add an hour
            if next_closest_15_minutes == 60:
                first_delivery_time = first_delivery_time.replace(minute=0)
                first_delivery_time += datetime.timedelta(hours=1)
            # Otherwise replace mintutes with next interval time
            else:
                first_delivery_time = first_delivery_time.replace(minute=next_closest_15_minutes)
            
            # Add 30 minutes buffer for restaurant to cook food
            first_delivery_time += datetime.timedelta(minutes=30)

            # Make each datetime object aware for database
            first_delivery_time.replace(tzinfo=utc)
            closing_time.replace(tzinfo=utc)

            # Create list of 15 minute delivery times
            while first_delivery_time < closing_time:
                first_delivery_time += datetime.timedelta(minutes=15)
                delivery_times.append(first_delivery_time.time())

            print(first_delivery_time, closing_time)
        return delivery_times if delivery_times else None


    def get_friendly_name(self):
        return self.friendly_name
    
    def __str__(self):
        return self.name
    

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

    restaurant = models.ForeignKey(
        "Restaurant", on_delete=CASCADE, related_name="hours")
    weekday = models.IntegerField(choices=WEEKDAYS)
    from_hour = models.TimeField()
    to_hour = models.TimeField()


# Menu Section
class MenuSection(models.Model):
    class Meta:
        verbose_name_plural = 'Menu Sections'

    restaurant = models.ForeignKey('Restaurant', on_delete=CASCADE)
    name = models.CharField(max_length=254)
    friendly_name = models.CharField(
        max_length=254, default="Please set friendly name")

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
