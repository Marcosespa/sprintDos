from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Obtiene un elemento del diccionario usando una clave."""
    return dictionary.get(key)