import datetime
from math import ceil
from statistics import mean
from django.db import models
from django.utils.timezone import utc
from django.db.models.deletion import CASCADE, SET_NULL

# Cuisine


class Cuisine(models.Model):
    name = models.CharField(max_length=254)
    icon_html = models.TextField(
        max_length=254, default="Please enter icon html")

    def __str__(self):
        return self.name


# Restaurant
class Restaurant(models.Model):
    cuisine = models.ForeignKey(
        'Cuisine', null=True, blank=True, on_delete=SET_NULL)
    name = models.CharField(max_length=254)
    friendly_name = models.CharField(
        max_length=254, default="Please set friendly name")
    description = models.TextField()
    rating = models.DecimalField(
        max_digits=3, decimal_places=2, null=True, blank=True)
    logo = models.ImageField(null=True, blank=True)
    cover_image = models.ImageField(null=True, blank=True)
    address_1 = models.CharField(
        max_length=254, default="Please enter address 1")
    address_2 = models.CharField(
        max_length=254, default="Please enter address 2", null=True, blank=True)
    post_code = models.CharField(
        max_length=254, default="Please enter post code")
    delivery_cost = models.DecimalField(
        max_digits=4, decimal_places=2, default="0.00")
    phone_number = models.DecimalField(
        max_digits=10, decimal_places=0, blank=False, null=False, default=0)

    def update_rating(self):
        orders = self.orders.all().exclude(rating__isnull=True)
        ratings = [order.rating for order in orders]
        average_rating = mean(ratings)
        self.rating = round(average_rating, 2)
        self.save()

    def get_opening_hours(self):
        try:
            weekday = datetime.datetime.today().weekday()
            opening_hours = self.hours.all()
            todays_opening_hours = opening_hours.filter(weekday=weekday)
            opening_time = str(todays_opening_hours[0].from_hour)[:-3]
            closing_time = str(todays_opening_hours[0].to_hour)[:-3]
            return f'{opening_time} - {closing_time}'
        except Exception:
            return None

    def get_opening_time(self):
        weekday = datetime.datetime.today().weekday()
        try:
            todays_opening_hours = self.hours.all().filter(weekday=weekday)
            opening_time = todays_opening_hours[0].from_hour
            return opening_time
        except Exception:
            return None

    def is_open_today(self):
        weekday = datetime.datetime.today().weekday()
        todays_opening_hours = self.hours.all().filter(weekday=weekday)
        return True if todays_opening_hours else False

    def is_open_now(self):
        now = datetime.datetime.now().time().replace(microsecond=0)
        weekday = datetime.datetime.today().weekday()
        try:
            todays_opening_hours = self.hours.all().filter(weekday=weekday)
            opening_time = todays_opening_hours[0].from_hour
            closing_time = todays_opening_hours[0].to_hour
            return True if self.is_open_today() and (closing_time > now >= opening_time) else False
        except Exception:
            return False

    def is_open_later_today(self):
        if self.is_open_today():
            # If restaurant currently open, then it will be open later (presuming it's not the final minute)
            if self.is_open_now():
                return True
            # Get/set variables
            now = datetime.datetime.now()
            weekday = datetime.datetime.today().weekday()
            today = datetime.datetime.today()
            opening_hours = self.hours.all()
            todays_opening_hours = opening_hours.filter(weekday=weekday)
            closing_time = str(todays_opening_hours[0].to_hour)
            # Convert to datetime
            closing_time = datetime.datetime.strptime(
                f'{today.date()} {closing_time}', "%Y-%m-%d %H:%M:%S")
            # If restaurant was open today, but has now closed, return False
            if now >= closing_time:
                return False
            # Else must be before restaurant is opening for the day, therefore true
            return True
        # Restaurant not open today at all
        return False

    def get_todays_delivery_times(self):
        delivery_times = []

        if self.is_open_today():
            # Get/set variables
            today = datetime.datetime.today()
            weekday = datetime.datetime.today().weekday()
            todays_opening_hours = self.hours.all().filter(weekday=weekday)
            opening_time = todays_opening_hours[0].from_hour
            closing_time = todays_opening_hours[0].to_hour

            # If closing time is midnight, replace with 23:59:59 for processing
            if datetime.time.strftime(closing_time, "%H:%M:%S") == "00:00:00":
                closing_time = datetime.time(hour=23, minute=59, second=59)

            # Convert from datetime.time to datetime.datetime object
            closing_time = datetime.datetime.strptime(
                f'{today.date()} {closing_time}', "%Y-%m-%d %H:%M:%S")
            opening_time = datetime.datetime.strptime(
                f'{today.date()} {opening_time}', "%Y-%m-%d %H:%M:%S")

            # Find next closest 15 minute interval (i.e. 15, 30, 45, 60)
            if self.is_open_now():
                first_delivery_time = today.now()
                next_closest_15_minutes = ceil(today.time().minute / 15) * 15
            else:
                first_delivery_time = opening_time
                next_closest_15_minutes = ceil(opening_time.minute / 15) * 15

            # If next 15 minute interval is on the next hour, remove minutes and add an hour
            if next_closest_15_minutes == 60:
                first_delivery_time = first_delivery_time.replace(minute=0)
                first_delivery_time += datetime.timedelta(hours=1)
            # Otherwise replace minutes with next interval time
            else:
                first_delivery_time = first_delivery_time.replace(
                    minute=next_closest_15_minutes)

            # Add 45 minutes buffer for restaurant to cook food etc.
            first_delivery_time += datetime.timedelta(minutes=45)

            # Add 45 minutes after restaurant stops taking orders for delivery time selection
            closing_time += datetime.timedelta(minutes=45)

            # Make each datetime object aware for database
            first_delivery_time.replace(tzinfo=utc)
            closing_time.replace(tzinfo=utc)

            # Create list of 15 minute delivery times
            while first_delivery_time < closing_time:
                delivery_times.append(first_delivery_time.time())
                first_delivery_time += datetime.timedelta(minutes=15)

        return delivery_times

    def get_friendly_name(self):
        return self.friendly_name

    def __str__(self):
        return self.name


# Opening Hours
class OpeningHours(models.Model):
    class Meta:
        ordering = ('weekday', 'from_hour')
        unique_together = ('weekday', 'from_hour', 'to_hour')
        verbose_name_plural = 'Opening Hours'

    # Referenced https://stackoverflow.com/questions/28450106/business-opening-hours-in-django
    weekdays = [
        (0, ("Monday")),
        (1, ("Tuesday")),
        (2, ("Wednesday")),
        (3, ("Thursday")),
        (4, ("Friday")),
        (5, ("Saturday")),
        (6, ("Sunday")),
    ]

    restaurant = models.ForeignKey(
        "Restaurant", on_delete=CASCADE, related_name="hours")
    weekday = models.IntegerField(choices=weekdays)
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
