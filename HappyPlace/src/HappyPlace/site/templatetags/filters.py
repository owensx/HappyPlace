from django import template
from django.template.defaultfilters import stringfilter
import ast

register = template.Library()

DAYSMAP = {'S':'Sunday'
    ,'M':'Monday'
    ,'T':'Tuesday'
    ,'W':'Wednesday'
    ,'R':'Thursday'
    ,'F':'Friday'
    ,'Y':'Saturday'}

@register.filter(name='beautifyUrl')
@stringfilter
def beautifyUrl(value):
    value = value[7:] #strip http://
    value = value if not value.startswith('www') else value[4:] #strip www
    value = value if not value.endswith('/') else value[:len(value)-1] #strip trailing slash
    return value


@register.filter(name='beautifyDays')
def beautifyDays(value):
    output = '|  ';
    
    for dayString in ast.literal_eval(value):
        output += DAYSMAP[dayString] + '  |  '
        
    return output