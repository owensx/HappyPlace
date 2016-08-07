from django import template
from django.template.defaultfilters import stringfilter
import ast
import re
from HappyPlace.site.models import HappyPlace

register = template.Library()

DAYSABBREVMAP = {'S':'Sunday'
    ,'M':'Monday'
    ,'T':'Tuesday'
    ,'W':'Wednesday'
    ,'R':'Thursday'
    ,'F':'Friday'
    ,'Y':'Saturday'}

DAYSINTMAP = {'6':'Sunday'
    ,'0':'Monday'
    ,'1':'Tuesday'
    ,'2':'Wednesday'
    ,'3':'Thursday'
    ,'4':'Friday'
    ,'5':'Saturday'}

def intToDayOfWeek(value):
    for key, entry in DAYSABBREVMAP.items():
        if DAYSINTMAP[str(value)] == entry:
            return key

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
        output += DAYSABBREVMAP[dayString] + '  |  '
        
    return output


@register.filter(name='formatStart')
# def formatStart(value):
#     if str(value) == '00:00:00':
#         return 'Midnight'
#     elif str(value) == '00:00:01':
#         return 'Open'        
#     else:
#         value = str(value)[1::-1][::-1]
#         value = int(value)
#         
#         value = value if value < 13 else value - 12
#         
#         return value

@register.filter(name='formatTime')
def formatTime(value):
    if str(value) == '00:00:00':
        return 'Midnight'
    elif str(value) == '00:00:01':
        return 'Open'        
    elif str(value) == '02:01:00':
        return 'Close'
    else:
        value = str(value)[1::-1][::-1]
        value = int(value)
        
        ampm = 'pm' if value > 11 else 'am'
        
        value = value if value < 13 else value - 12
        
        return str(value)+ampm

@register.filter(name='formatTimeRange')
def formatTimeRange(start, end):
    if start == 'Open' and end=='Close':
        return 'All Day'
    else:
        return str(start) + '-' + str(end)
    
@register.filter(name='beautifyPhone')
def beautifyPhone(phone):
    phone = re.sub('[\(\.\)\-\s]','',phone)
    return phone