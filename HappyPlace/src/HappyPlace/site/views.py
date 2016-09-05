import os
from googleplaces import GooglePlaces, types, lang
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from HappyPlace.site.models import *
from uuid import uuid4
from django.http.response import HttpResponseBadRequest, HttpResponse
from datetime import datetime, time, timedelta
from HappyPlace.site.templatetags.filters import *
from django.core import serializers
import json
from django.template.response import TemplateResponse
from django.contrib.staticfiles.templatetags.staticfiles import static
from HappyPlace import settings

def SubmissionFormsView(request):
    
    cityForm = CityForm()
    happyPlaceForm = HappyPlaceForm()
    happyHourForm = HappyHourForm()
    
    context = {
               'cityForm' : cityForm
               , 'happyPlaceForm' : happyPlaceForm
               , 'happyHourForm' : happyHourForm
               }        
    return render(request, 'submit.html', context)

def AddCity(request):
    if request.method == 'POST':
        print("received city form POST")
        form = CityForm(request.POST)
         
        if form.is_valid():
            print ("form validated")
            idToInsert = generateId(City.objects)
             
            city = City(
                    id=idToInsert
                    ,name=form.cleaned_data['name']
                    ,offset=form.cleaned_data['offset']
                    )
            
            city.save()
            print("city saved successfully")
            
        else:
            print('could not validate form: ' + str(form.errors.as_data()))
            context = {
               'happyPlaceForm' : form
               , 'happyHourForm' : HappyHourForm()
               }        
            return render(request, 'submit.html', context)
            
    return HttpResponseRedirect('/submit')
def AddHappyPlace(request):
    if request.method == 'POST':
        print("received happyPlace form POST")
        form = HappyPlaceForm(request.POST)

        if form.is_valid():
            print ("form validated")
            idToInsert = generateId(HappyPlace.objects)

            if not form.cleaned_data['site'] == '':
                print('site field populated: ' + form.cleaned_data['site'])                            
                if not form.cleaned_data['site'].startswith('http'):
                    print('prepending http...')
                    form.cleaned_data['site'] = 'http://' + form.cleaned_data['site']
                
            happyPlace = HappyPlace(
                        id=idToInsert
                      , name=form.cleaned_data['name']
                      , address=form.cleaned_data['address']
                      , neighborhood=form.cleaned_data['neighborhood']
                      , city=form.cleaned_data['city']
                      
                      , cross=None if form.cleaned_data['cross'] == '' else form.cleaned_data['cross']
                      , site=None if form.cleaned_data['site'] == '' else form.cleaned_data['site']
                      , phone=None if form.cleaned_data['phone'] == '' else beautifyPhone(form.cleaned_data['phone'])
                      , latitude=None if form.cleaned_data['latitude'] == '' else form.cleaned_data['latitude']
                      , longitude=None if form.cleaned_data['longitude'] == '' else form.cleaned_data['longitude']
                    )
            
            print("happyPlace created: ")
            print("\tid: "+ str(happyPlace.id))
            print("\tname: "+ str(happyPlace.name))
            print("\taddress: "+ str(happyPlace.address))
            print("\tneighborhood: "+ str(happyPlace.neighborhood))
            print("\tcity: "+ str(happyPlace.city))
            print("\tcross: "+ str(happyPlace.cross))
            print("\tsite: "+ str(happyPlace.site))
            print("\tphone: "+ str(happyPlace.phone))
            print("\tlatitude: "+ str(happyPlace.latitude))
            print("\tlongitude: "+ str(happyPlace.longitude))
            
            happyPlace.save()
            print("happyPlace saved successfully")
            
            return HttpResponseRedirect('/submit')    
        
        else:
            print('could not validate form: ' + str(form.errors.as_data()))
            context = {
               'happyPlaceForm' : form
               , 'happyHourForm' : HappyHourForm()
               }        
            return render(request, 'submit.html', context)
        
def AddHappyHour(request):
    if request.method == 'POST':
        print("received happyHour form POST")
        form = HappyHourForm(request.POST)
            
        if form.is_valid():            
            print ("form validated")            
            idToInsert = generateId(HappyHour.objects)
            
            happyHour = HappyHour(
                    id=idToInsert
                    ,notes=form.cleaned_data['notes']
                    ,days=form.cleaned_data['days']
                    ,start=form.cleaned_data['start']
                    ,end=form.cleaned_data['end']
                    ,happyPlace=form.cleaned_data['happyPlace']
                    ,beer=form.cleaned_data['beer']
                    ,wine_glass=form.cleaned_data['wine_glass']
                    ,wine_bottle=form.cleaned_data['wine_bottle']
                    ,shot_beer=form.cleaned_data['shot_beer']
                    ,well=form.cleaned_data['well']
                    ,display_notes=form.cleaned_data['display_notes']
                    )
            
            print("happyHour created: ")
            print("\tid: "+ str(happyHour.id))
            print("\tnotes: "+ str(happyHour.notes))
            print("\tdays: "+ str(happyHour.days))
            print("\tstart: "+ str(happyHour.start))
            print("\tend: "+ str(happyHour.end))
            print("\thappyPlace: "+ str(happyHour.happyPlace.name))
            
            happyHour.save()
            print("happyHour saved")
            
            return HttpResponseRedirect('/submit')
        
        else:
            print('could not validate form: ' + str(form.errors.as_data()))
            context = {
               'happyPlaceForm' : HappyPlaceForm()
               , 'happyHourForm' : form
               }        
            return render(request, 'submit.html', context)
            
def Home(request):
    mobileFlag = request.POST.get('mobileFlag')
    mobileOverride = request.POST.get('mobileOverride')
    #mapDisplay = 'initial' if request.POST.get('mapDisplay') == None else request.POST.get('mapDisplay')
    #tableDisplay = request.POST.get('tableDisplay')
    rightNowFlag = 'true' if request.POST.get('currentTimeOnly') is not None else 'false'
    
    allActiveHappyPlaces = HappyPlace.objects.filter(active=True).exclude(place_id__isnull=True)
    allCities = sorted(set(happyPlace.city.name for happyPlace in allActiveHappyPlaces))
    
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
            happyPlaces = allActiveHappyPlaces.filter(city=City.objects.get(name=request.POST.get('city')))
        else:
            print('returning all happyPlaces in ' + request.POST.get('neighborhood') + ', ' + request.POST.get('city'))
            happyPlaces = allActiveHappyPlaces.filter(neighborhood=request.POST.get('neighborhood'))
    else:
        happyPlaces = allActiveHappyPlaces

    if request.POST.get('currentTimeOnly') and not request.POST.get('city') == 'defaultCity':
        print('only returning happyHours happening now')
        happyHours = [happyHour for happyPlace in happyPlaces for happyHour in happyPlace.happyHours.all()]
        
        currentLocalDatetime = datetime.utcnow() + timedelta(hours=happyHours[0].happyPlace.city.offset)
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
    
    
    happyPlaces = sorted(happyPlaces,key=lambda happyPlace:happyPlace.neighborhood);
    
    if len(happyPlaces) == 0:
        return HttpResponseRedirect('/error/')
    context = {
               'happyPlaces' : happyPlaces
               , 'mapCenter' : json.dumps(getAverageLatLng(happyPlaces))
               , 'dayPairs' : DAYS
               , 'today' : intToDayOfWeek((datetime.utcnow() + timedelta(hours=happyPlaces[0].city.offset)).weekday())
               , 'cities' : allCities
               , 'lastSelectedCity' : request.POST.get('city') if request.POST.get('city') is not None else 'defaultCity'
               , 'lastSelectedNeighborhood' : request.POST.get('neighborhood') if request.POST.get('neighborhood') is not None else 'all'
               , 'mobileFlag' : mobileFlag
               , 'mobileOverride' : mobileOverride
               , 'rightNowFlag' : rightNowFlag
               #, 'mapDisplay' : mapDisplay
               #, 'tableDisplay' : tableDisplay
               }
    
    if mobileFlag == 'true':
        print('rendering mobile template')
        return TemplateResponse(request, 'home_mobile.html', context)
    
    return TemplateResponse(request, 'home.html', context)

def Error(request):
    
    return render(request, 'error.html')


def getNeighborhoodsForCity(request, cityToSearch):
    #reconstruct spaces in search parameter
    cityToSearch = cityToSearch.replace('_', ' ')
    city = City.objects.get(name=cityToSearch)
    happyPlacesInCity = city.happyPlaces.all().filter(active=1)
    
    allNeighborhoods = (happyPlace.neighborhood for happyPlace in happyPlacesInCity)
    uniqueNeighborhoods = sorted(set(allNeighborhoods))
    
    return HttpResponse(json.dumps(list(uniqueNeighborhoods)), content_type="application/javascript")

def getPhotos(request, location):    
    if location.endswith('all'):
        location = location[:len(location)-3]
        
    folderContents=os.listdir(os.path.join(settings.STATIC_ROOT + 'photos',location))
    photos=list(name for name in folderContents if (os.path.isfile(os.path.join(settings.STATIC_ROOT + 'photos', location + "/" + name))) and name.endswith('jpg'))
    
    return HttpResponse(json.dumps(len(photos)), content_type="application/javascript")

def getAverageLatLng(happyPlaces):
    sumLat = 0
    sumLng = 0
    latLngs = [happyPlace.latLng for happyPlace in happyPlaces]
    
    for latLng in latLngs:        
        sumLat += latLng['lat']
        sumLng += latLng['lng']
    
    return list([float(sumLat/len(happyPlaces)), float(sumLng/len(happyPlaces))])

def generateId(objects):    
    generatedId = uuid4().int % 1000000000

    while objects.filter(id=generatedId):
        generatedId = uuid4().int % 1000000000
    
    print('generated id: ' + str(generatedId))
    return generatedId