from django import template

register = template.Library()

@register.filter
def modulo(num, val):
    # Return the remainder of division
    return num % val

@register.filter
def multiply(value, arg):
    # Multiply two values (handles iterables by length)
    try:
        v = value
        a = arg
        # handle iterables (use their length)
        if hasattr(value, '__len__') and not isinstance(value, (str, bytes)):
            try:
                v = len(value)
            except Exception:
                v = value
        if hasattr(arg, '__len__') and not isinstance(arg, (str, bytes)):
            try:
                a = len(arg)
            except Exception:
                a = arg
        return int(v) * int(a)
    except Exception:
        return 0

@register.filter
def divide(value, arg):
    # Divide two values (handles iterables by length)
    def _to_number(x):
        # If iterable (list, queryset), use its length; try count() if available
        try:
            if hasattr(x, '__len__') and not isinstance(x, (str, bytes)):
                return len(x)
            if hasattr(x, 'count') and callable(getattr(x, 'count')):
                try:
                    return x.count()
                except Exception:
                    pass
            return float(x)
        except Exception:
            return None

    try:
        v = _to_number(value)
        a = _to_number(arg)
        if v is None or a is None:
            return 0
        if a == 0:
            return 0
        return v / a
    except Exception:
        return 0
