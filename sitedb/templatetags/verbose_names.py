from django import template

register = template.Library()


@register.simple_tag
def get_verbose_field_name(instance, field_name):
    """
    Returns verbose_name for a field.
    """
    return instance._meta.get_field(field_name).verbose_name.title()


@register.filter
def verbose_name(obj):
    return obj._meta.verbose_name


@register.filter
def verbose_name_plural(obj):
    return obj._meta.verbose_name_plural


@register.simple_tag
def subtract(a, b):
    if (not a) or (not b):
        return 0
    return (a-b).days


@register.simple_tag
def model_verbose_name(value):
    # Django template filter which returns the verbose name of a model.
    # Note: I set my verbose_name the same as the plural, so I only need one tag.
    if hasattr(value, 'model'):
        value = value.model
    return value._meta.verbose_name