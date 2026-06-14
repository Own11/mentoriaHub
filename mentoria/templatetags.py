from django import template

register = template.Library()

@register.filter
def modulo(num, val):
    """Получить остаток от деления"""
    return num % val

@register.filter
def multiply(value, arg):
    """Умножить значение"""
    return int(value) * int(arg)

@register.filter
def divide(value, arg):
    """Разделить значение"""
    try:
        return int(value) / int(arg)
    except (ValueError, ZeroDivisionError):
        return 0
