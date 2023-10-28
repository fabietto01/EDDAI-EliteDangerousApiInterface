from django import template

register = template.Library()

@register.filter(name='get_attr')
def get_attr(obj, attr:str):
    return getattr(obj, attr, '')