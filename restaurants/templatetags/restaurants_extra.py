import math
from django import template
from django.shortcuts import get_object_or_404
from restaurants.models import Restaurant

register = template.Library()


@register.filter(name='remove_decimals')
def remove_decimals(value):
    return math.floor(value)


@register.filter(name='create_list_of_length_number')
def create_list_of_length_number(number):
    list = [*range(0, number, 1)]
    return list


@register.filter(name='remove_whole_number')
def remove_whole_number(value):
    num = math.floor(value)
    return value - num


@register.filter(name='count')
def count(object):
    return len(object)


@register.filter(name='get_number_of_orders_with_rating')
def get_number_of_orders_with_rating(orders):
    orders = orders.exclude(rating__isnull=True)
    return len(orders)
