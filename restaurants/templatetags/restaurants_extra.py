from django import template
import math

register = template.Library()


@register.filter(name='remove_decimals')
def remove_decimals(value):
    return math.floor(value)


@register.filter(name='create_list_from_number')
def create_list_from_number(number):
    list = [*range(0, number, 1)]
    return list


@register.filter(name='remove_whole_number')
def remove_whole_number(value):
    num = math.floor(value)
    return value - num
