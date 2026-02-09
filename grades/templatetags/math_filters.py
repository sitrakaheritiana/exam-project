from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
    """Multiplie value par arg"""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0
