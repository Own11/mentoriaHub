from django import template

register = template.Library()

@register.filter
def modulo(num, val):
    # Return remainder of division
    return num % val

@register.filter
def multiply(value, arg):
    # Multiply two values
    return int(value) * int(arg)

@register.filter
def divide(value, arg):
    # Divide two values, return 0 on error
    try:
        return int(value) / int(arg)
    except (ValueError, ZeroDivisionError):
        return 0
