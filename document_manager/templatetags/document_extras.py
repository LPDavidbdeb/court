from django import template

register = template.Library()

@register.filter(name='model_name')
def model_name(value):
    """Returns the name of the model for a given object."""
    return value.__class__.__name__.lower()

@register.filter(name='get_item')
def get_item(dictionary, key):
    """
    Allows accessing a dictionary item by a key that is a variable.
    Especially useful when the key is an object in a loop.
    """
    return dictionary.get(key)

@register.filter(name='multiply')
def multiply(value, arg):
    """Multiplies the value by the arg."""
    try:
        return int(value) * int(arg)
    except (ValueError, TypeError):
        return ''
