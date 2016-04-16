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

@register.filter(name='formatStart')
def formatStart(value):
    value = str(value)[1::-1][::-1]
    value = int(value)
    value = value if value < 13 else value - 12
    value = value if not str(value).startswith('0') else value[1:]

    return value

@register.filter(name='formatEnd')
def formatEnd(value):
    value = str(value)[1::-1][::-1]
    value = int(value)
    
    ampm = 'pm' if value > 11 else 'am'
    
    value = value if value < 13 else value - 12
    value = value if not str(value).startswith('0') else value[1:]
                    
    return str(value)+ampm
