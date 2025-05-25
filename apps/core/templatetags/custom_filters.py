from django import template

register = template.Library()

@register.filter
def div(value, arg):
    try:
        return (float(value) / float(arg)) * 100 if float(arg) != 0 else 0
    except (ValueError, TypeError, ZeroDivisionError):
        return 0

@register.filter
def floatval(value):
    try:
        return float(value)
    except (ValueError, TypeError):
        return 0

@register.filter
def cap(value, max_value):
    try:
        return min(float(value), float(max_value))
    except (ValueError, TypeError):
        return 0

@register.filter
def budget_color(value):
    try:
        value = float(value)
        if value < 80:
            return "bg-success"
        elif value < 100:
            return "bg-warning"
        else:
            return "bg-danger"
    except:
        return ""