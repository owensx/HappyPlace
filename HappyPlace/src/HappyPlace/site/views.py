import os
import json
from HappyPlace.site.utils import *
from googleplaces import GooglePlaces, types, lang
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from HappyPlace.site.models import *
from datetime import datetime, time, timedelta
from HappyPlace.site.templatetags.filters import *
from django.core import serializers
from django.template.response import TemplateResponse
from django.contrib.staticfiles.templatetags.staticfiles import static
from HappyPlace import settings
from django.core.urlresolvers import reverse

def Submit(request):
    context = {
               'displayStateSumbit': 'initial'
               , 'displayCitySumbit': 'none'
               , 'displayHappyPlaceSumbit': 'none'
               , 'displayHappyHourSumbit': 'none'
               }
    
    if request.method == 'GET':
        context['stateForm'] = StateForm()
        
    elif request.method == 'POST':
        formType = request.POST.get('formType')

        if formType == 'stateForm':
            stateForm = StateForm(request.POST)
            
            if stateForm.is_valid():
                formData = stateForm.cleaned_data
                
                state = formData['state']
                             
                cityForm = CityForm()                
                initCityFormView(cityForm, state, context)
                
        elif formType == 'cityForm':
            stateId = request.POST.get('stateId')
            
            cityForm = CityForm(request.POST)
            state = State.objects.get(id=stateId)
            
            if cityForm.is_valid():
                formData = cityForm.cleaned_data
                        
                if not formData['city']:
                    city = saveNewCity(formData, state)
                else:
                    city = formData['city']
                
                happyPlaceForm = HappyPlaceForm()
                initHappyPlaceFormView(happyPlaceForm, city, context)
             
            else:
                initCityFormView(cityForm, state, context)
                   
        elif formType == 'happyPlaceForm':
            cityId = request.POST.get('cityId')
            
            happyPlaceForm = HappyPlaceForm(request.POST)
            city = City.objects.get(id=cityId)
            
            if happyPlaceForm.is_valid():
                formData = happyPlaceForm.cleaned_data
                    
                happyPlace = saveNewHappyPlace(formData, city)                
                    
                happyHourForm = HappyHourForm()                
                initHappyHourFormView(happyHourForm, happyPlace, context)
            
            else:
                initHappyPlaceFormView(happyPlaceForm, city, context)
            
        elif formType == 'happyHourForm':
            happyHourForm = HappyHourForm(request.POST)
            happyPlace = HappyPlace.objects.get(id=request.POST.get('happyPlaceId'))
            
            if happyHourForm.is_valid():
                formData = happyHourForm.cleaned_data
                
                saveNewHappyHour(formData, happyPlace)
                
                return HttpResponseRedirect(reverse('home'))
            
            else:
                initHappyHourFormView(happyHourForm, happyPlace, context)
                
    return render(request, 'submit.html', context)

def Home(request):
    mobileFlag = request.POST.get('mobileFlag')
    mobileOverride = request.POST.get('mobileOverride')
    mapDisplay = 'initial' if request.POST.get('mapDisplay') == None else request.POST.get('mapDisplay')
    tableDisplay = request.POST.get('tableDisplay')
    rightNowFlag = 'true' if request.POST.get('currentTimeOnly') is not None else 'false'
    
    allActiveHappyPlaces = HappyPlace.objects.filter(active=True).exclude(latitude__isnull=True)
    allCities = sorted(set(happyPlace.neighborhood.city.name for happyPlace in allActiveHappyPlaces))
    
    if request.method == 'GET':
        context = {
                   'cities' : allCities
                   }
        return TemplateResponse(request, 'splash.html', context)
    
    if request.method == 'POST':
        print('received POST on home view')
        if request.POST.get('city') == 'defaultCity':
            print('no city selected, returning all happyPlaces')
            happyPlaces = allActiveHappyPlaces           
        elif request.POST.get('neighborhood') == 'all' or request.POST.get('neighborhood') == None:
            print('no neighborhood selected, returning all happyPlaces in ' + request.POST.get('city'))
            happyPlaces = list(filter(lambda happyPlace: happyPlace.neighborhood in list(City.objects.get(name=request.POST.get('city')).neighborhoods.all()), allActiveHappyPlaces))
        else:
            print('returning all happyPlaces in ' + request.POST.get('neighborhood') + ', ' + request.POST.get('city'))
            happyPlaces = list(filter(lambda happyPlace: happyPlace.neighborhood.name == request.POST.get('neighborhood'), allActiveHappyPlaces))
    else:
        happyPlaces = allActiveHappyPlaces

    if request.POST.get('currentTimeOnly') and not request.POST.get('city') == 'defaultCity' and happyPlaces:
        print('only returning happyHours happening now')
        happyHours = [happyHour for happyPlace in happyPlaces for happyHour in happyPlace.happyHours.all()]
        
        currentLocalDatetime = datetime.utcnow()
        print(currentLocalDatetime)
        currentLocalDate = currentLocalDatetime.date()
        currentWeekdayInt = currentLocalDatetime.weekday()
        
        today = intToDayOfWeek(currentWeekdayInt)

        happyHours = [happyHour for happyHour in happyHours if today in happyHour.days]
        
        happyHoursAllDay = [happyHour for happyHour in happyHours if
                            str(happyHour.end) == '02:01:00'and str(happyHour.start) == '00:00:01'
                           ]
        
        happyHoursSameDay = [happyHour for happyHour in happyHours if
                            (
                             happyHour.end > happyHour.start
                             and (currentLocalDatetime >= datetime.combine(currentLocalDate, happyHour.start))
                             and (currentLocalDatetime <= datetime.combine(currentLocalDate, happyHour.end))
                            )
                            ]
        happyHoursOvernight = [happyHour for happyHour in happyHours if
                            (
                             happyHour.end < happyHour.start
                             and 
                             (
                              (currentLocalDatetime >= datetime.combine(currentLocalDate, happyHour.start))
                              or (currentLocalDatetime <= datetime.combine(currentLocalDate, happyHour.end))
                             )
                            )
                            ]
        
        if mobileFlag == 'true':            
            happyHoursSameDay = [happyHour for happyHour in happyHours if
                            (
                             happyHour.end > happyHour.start
                             and (currentLocalDatetime >= (datetime.combine(currentLocalDate, happyHour.start) - timedelta(minutes=10)))
                             and (currentLocalDatetime <= datetime.combine(currentLocalDate, happyHour.end))
                            )
                            ]
        
        allHappyHours = happyHoursAllDay + happyHoursSameDay + happyHoursOvernight
        #allHappyHours = allHappyHours.order_by('start')
        
        happyPlaces = list(set(happyHour.happyPlace for happyHour in allHappyHours))
    
    
    happyPlaces = sorted(happyPlaces,key=lambda happyPlace: happyPlace.neighborhood.name);

    if len(happyPlaces) == 0:
        return HttpResponseRedirect('/error/')
    
    context = {
               'happyPlaces' : happyPlaces
               , 'mapCenter' : json.dumps(getAverageLatLng(happyPlaces))
               , 'dayPairs' : DAYS
               , 'today' : intToDayOfWeek((datetime.utcnow() + timedelta(hours=happyPlaces[0].neighborhood.city.state.offset)).weekday())
               , 'cities' : allCities
               , 'lastSelectedCity' : request.POST.get('city') if request.POST.get('city') is not None else 'defaultCity'
               , 'lastSelectedNeighborhood' : request.POST.get('neighborhood') if request.POST.get('neighborhood') is not None else 'all'
               , 'mobileFlag' : mobileFlag
               , 'mobileOverride' : mobileOverride
               , 'rightNowFlag' : rightNowFlag
               , 'mapDisplay' : mapDisplay
               , 'tableDisplay' : tableDisplay
               }
    
    if mobileFlag == 'true':
        print('rendering mobile template')
        return TemplateResponse(request, 'home_mobile.html', context)
    
    return TemplateResponse(request, 'home.html', context)

def Error(request):
    
    return render(request, 'error.html')


                
# def SubmitState(request):
#     if request.method == 'POST':
#         stateForm = StateForm(request.POST)
#         
#         if stateForm.is_valid():
#             
#             stateName = stateForm.cleaned_data['state'].name
#             context = {
#                        'stateId' : State.objects.all().get(name=stateName).id
#                        }
#             
#             return HttpResponseRedirect(reverse('submitCityForState', kwargs=context))
#         else:
#             print('could not validate form: ' + str(stateForm.errors.as_data()))
#             context = {
#                'stateForm' : stateForm
#                }        
#             
#         
#     stateForm = StateForm()
#     
#     context = {
#                'stateForm' : stateForm
#                }
#        
#     return render(request, 'submitStart.html', context)
# 
# def SubmitCityForState(request, stateId):
#     if request.method == 'POST':
#         cityForm = CityForm(request.POST)
#         
#         if cityForm.is_valid():
#             print ("form validated")
#             
#             if cityForm.cleaned_data['city'] == None:
#                 cityName = cityForm.cleaned_data['name']
#                 
#                 if str(cityName) in list(city.name for city in City.objects.all()):
#                     print('Already have this City!')
#                     
#                     cityId = City.objects.all().get(name=cityName).id
#                     context = {
#                                'cityId' : cityId
#                                }   
#                     return HttpResponseRedirect(reverse('submitHappyPlaceForCity', kwargs=context))
#                 else:
#                     idToInsert = generateId(City.objects)
#                     state=State.objects.all().get(id=stateId)
#                     city = City(
#                             id=idToInsert
#                             ,name=cityName
#                             ,state=state
#                             ,timeUpdated=timezone.now()
#                             )
#                      
#                     city.save()
#                     print("city saved successfully")
#                 
#                 context = {
#                            'cityId' : city.id
#                            }   
#                 return HttpResponseRedirect(reverse('submitHappyPlaceForCity', kwargs=context))
#             
#             else:
#                 city = cityForm.cleaned_data['city']
#                 context = {
#                            'cityId' : city.id
#                            }   
#                 return HttpResponseRedirect(reverse('submitHappyPlaceForCity', kwargs=context))
#         else:
#             print('could not validate form: ' + str(cityForm.errors.as_data()))
#             context = {
#                        'cityForm' : cityForm
#                        }        
#             return render(request, 'submitCity.html', context)
#     
#     cityForm = CityForm()
#     cityForm.fields['city'].queryset = City.objects.filter(state=State.objects.filter(id=stateId)).order_by('name')
# 
#     context = {
#                 'cityForm' : cityForm
#                 , 'stateId' : stateId
#                }
#              
#     return render(request, 'submitCity.html', context)
# 
# def SubmitHappyPlaceForCity(request, cityId):
#     if request.method == 'POST':
#         print("received happyPlace form POST")
#         happyPlaceForm = HappyPlaceForm(request.POST)
# 
#         if happyPlaceForm.is_valid():
#             print ("form validated")
#             
#             if happyPlaceForm.cleaned_data['happyPlace'] == None:
#                 
#                 placeId = happyPlaceForm.cleaned_data['place_id']
#                 
#                 if placeId in list(happyPlace.place_id for happyPlace in HappyPlace.objects.all()):
#                     print('Already have this HappyPlace!')
#                     
#                     happyPlaceId = HappyPlace.objects.all().get(place_id=placeId)
#                     context = {
#                                'happyPlaceId' : happyPlaceId
#                                }   
#                     return HttpResponseRedirect(reverse('submitHappyHourForHappyPlace', kwargs=context))
#     
#                 happyPlace = HappyPlace(
#                             id=generateId(HappyPlace.objects)
#                           , name=happyPlaceForm.cleaned_data['name']
#                           , address=happyPlaceForm.cleaned_data['address']
#                           , neighborhood=happyPlaceForm.cleaned_data['neighborhood']
#                           , city=happyPlaceForm.cleaned_data['city']
#                           
#                           , cross=None if happyPlaceForm.cleaned_data['cross'] == '' else happyPlaceForm.cleaned_data['cross']
#                           , site=None if happyPlaceForm.cleaned_data['site'] == '' else happyPlaceForm.cleaned_data['site']
#                           , phone=None if happyPlaceForm.cleaned_data['phone'] == '' else beautifyPhone(happyPlaceForm.cleaned_data['phone'])
#                           , latitude=None if happyPlaceForm.cleaned_data['latitude'] == '' else happyPlaceForm.cleaned_data['latitude']
#                           , longitude=None if happyPlaceForm.cleaned_data['longitude'] == '' else happyPlaceForm.cleaned_data['longitude']
#                           
#                           , place_id=happyPlaceForm.cleaned_data['place_id']
#                         )
#                 
#                 if request.POST.get('active'):
#                     happyPlace.active = True
#                     
#                 print("happyPlace created: ")
#                 print("\tid: "+ str(happyPlace.id))
#                 print("\tname: "+ str(happyPlace.name))
#                 print("\taddress: "+ str(happyPlace.address))
#                 print("\tneighborhood: "+ str(happyPlace.neighborhood))
#                 print("\tcity: "+ str(happyPlace.city))
#                 print("\tcross: "+ str(happyPlace.cross))
#                 print("\tsite: "+ str(happyPlace.site))
#                 print("\tphone: "+ str(happyPlace.phone))
#                 print("\tlatitude: "+ str(happyPlace.latitude))
#                 print("\tlongitude: "+ str(happyPlace.longitude))
#                 print("\tplaceId: "+ str(happyPlace.place_id))
#                 
#                 #happyPlace.save()
#                 print("happyPlace saved successfully")
#                 
#                 context = {
#                            'happyPlaceId' : happyPlace.id
#                            }
#                 
#                 return HttpResponseRedirect(reverse('submitHappyHourForHappyPlace', kwargs=context))   
#         
#         else:
#             print('could not validate form: ' + str(happyPlaceForm.errors.as_data()))
#             context = {
#                'happyPlaceForm' : happyPlaceForm
#                , 'happyHourForm' : HappyHourForm()
#                }        
#             return render(request, 'submitHappyPlace.html', context)
#      
#     happyPlaceForm = HappyPlaceForm()
#     happyPlaceForm.fields['happyPlace'].queryset = HappyPlace.objects.filter(city=City.objects.filter(id=cityId)).order_by('name')
#         
#     context = {
#                'cityId' : cityId
#                 , 'happyPlaceForm' : happyPlaceForm
#                 }
#     return render(request, 'submitHappyPlace.html', context)
#         
# def SubmitHappyHourForHappyPlace(request, happyPlaceId):
#     if request.method == 'POST':
#         print("received happyHour form POST")
#         form = HappyHourForm(request.POST)
#             
#         if form.is_valid():            
#             print ("form validated")            
#             idToInsert = generateId(HappyHour.objects)
#             
#             happyHour = HappyHour(
#                     id=idToInsert
#                     ,notes=form.cleaned_data['notes']
#                     ,days=form.cleaned_data['days']
#                     ,start=form.cleaned_data['start']
#                     ,end=form.cleaned_data['end']
#                     ,happyPlace=form.cleaned_data['happyPlace']
#                     ,beer=form.cleaned_data['beer']
#                     ,wine_glass=form.cleaned_data['wine_glass']
#                     ,wine_bottle=form.cleaned_data['wine_bottle']
#                     ,shot_beer=form.cleaned_data['shot_beer']
#                     ,well=form.cleaned_data['well']
#                     ,display_notes=form.cleaned_data['display_notes']
#                     )
#             
#             print("happyHour created: ")
#             print("\tid: "+ str(happyHour.id))
#             print("\tnotes: "+ str(happyHour.notes))
#             print("\tdays: "+ str(happyHour.days))
#             print("\tstart: "+ str(happyHour.start))
#             print("\tend: "+ str(happyHour.end))
#             print("\thappyPlace: "+ str(happyHour.happyPlace.name))
#             
#             happyHour.save()
#             print("happyHour saved")
#             
#             return HttpResponseRedirect('/submit')
#         
#         else:
#             print('could not validate form: ' + str(form.errors.as_data()))
#             context = {
#                'happyPlaceForm' : HappyPlaceForm()
#                , 'happyHourForm' : form
#                }        
#             return render(request, 'submit.html', context)
#     
#     happyHourForm = HappyHourForm()
#     
#     context = {
#                'happyHourForm' : happyHourForm
#                 }
#     return render(request, 'submitHappyHour.html', context)
#         