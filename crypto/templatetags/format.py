from django import template
from django.template.defaulttags import register
import timeago, datetime
import pytz

now = datetime.datetime.now() + datetime.timedelta(seconds=60 * 3.4)
date = datetime.datetime.now()

register = template.Library()


@register.filter(name='format')
def format(value, fmt):
    return fmt.format(value)

@register.filter('intspace')
def int_format(value, decimal_points=3, seperator=u','):
    value = str(value)
    if len(value) <= decimal_points:
        return value
    # say here we have value = '12345' and the default params above
    parts = []
    while value:
        parts.append(value[-decimal_points:])
        value = value[:-decimal_points]
    # now we should have parts = ['345', '12']
    parts.reverse()
    # and the return value should be u'12.345'
    return seperator.join(parts)

@register.filter('datex')
def change_data(value):
    value = str(value)
    new_value = value[0:10]
    return new_value

@register.filter('btc')
def btc(value):
    return f"₿ {value:.8f}"

@register.filter('btc3')
def btc3(value):
    return f"₿ {value:.3f}"

@register.filter('datextime')
def datextime(value):
    value = str(value)
    new_value = value[0:10]+" "+value[11:16]
    return f"{new_value}"

@register.filter('usd2')
def usd2(value):
    return f" ${value:.2f}"

@register.filter('cala')
def cala(value):
    return f"{int(value)}"

@register.filter('usd3')
def usd3(value):
    return f"${value:.4f}"

@register.filter('procent')
def procent(value):
    return f"{value:.1f}%"

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter(name='lookup')
def lookup(value, arg):
    return value[arg]

@register.filter('volm')
def volm(value, arg):
    try:
        return (float(value) / int(arg))*100
    except (ValueError, ZeroDivisionError):
        return None