from django import template

register = template.Library()


@register.filter
def get_field(obj, field_name):
    return getattr(obj, field_name)
