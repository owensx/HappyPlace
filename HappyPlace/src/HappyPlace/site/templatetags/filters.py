from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter(name='stripHttp')
@stringfilter
def stripHttp(value):
    value.find('http://')
    return value[7:]

