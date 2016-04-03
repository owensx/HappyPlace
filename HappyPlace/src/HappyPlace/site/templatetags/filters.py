from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter(name='stripHttp')
@stringfilter
def stripHttp(value):
    value = value[7:] #strip http://
    value = value if not value.startswith('www') else value[4:] #strip www
    value = value if not value.endswith('/') else value[:len(value)-1] #strip trailing slash
    return value

