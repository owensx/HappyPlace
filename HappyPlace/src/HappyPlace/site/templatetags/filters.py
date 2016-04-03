from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter(name='stripHttp')
@stringfilter
def stripHttp(value):
    value = value[7:]
    return value if not value.startswith('www') else value[4:]

