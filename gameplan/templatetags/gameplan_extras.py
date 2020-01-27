from django import template

register = template.Library()


@register.filter
def get_params(dictionary, key):
    return dictionary.getlist(key)
