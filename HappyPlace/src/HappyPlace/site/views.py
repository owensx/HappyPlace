import os
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from HappyPlace.site.models import *
from uuid import uuid4
from django.http.response import HttpResponseBadRequest, HttpResponse
from datetime import datetime, time, timedelta
from HappyPlace.site.templatetags.filters import *
from django.core import serializers
import json

def SubmissionFormsView(request):
    happyPlaceForm = HappyPlaceForm()
    happyHourForm = HappyHourForm()
    
    context = {
               'happyPlaceForm' : happyPlaceForm
               , 'happyHourForm' : happyHourForm
               }        
    return render(request, 'submit.html', context)

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
                      , phone=None if form.cleaned_data['phone'] == '' else form.cleaned_data['phone']
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
            
            return HttpResponseRedirect('/home.html')    
        
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
                    ,happyPlace= form.cleaned_data['happyPlace']
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
            
            return HttpResponseRedirect('/home.html')
        
        else:
            print('could not validate form: ' + str(form.errors.as_data()))
            context = {
               'happyPlaceForm' : HappyPlaceForm()
               , 'happyHourForm' : form
               }        
            return render(request, 'submit.html', context)
            
def Home(request):
    allHappyPlaces = HappyPlace.objects.all()
    allCities = sorted(set(happyPlace.city.name for happyPlace in allHappyPlaces))
    
    if request.method == 'POST':
        print('received POST on home view')
        if request.POST.get('city') == 'defaultCity':
            print('no city selected, returning all happyPlaces')
            happyPlaces = allHappyPlaces           
        elif request.POST.get('neighborhood') == 'all':
            print('no neighborhood selected, returning all happyPlaces in ' + request.POST.get('city'))
            happyPlaces = City.objects.get(name=request.POST.get('city')).happyPlaces.all()
        else:
            print('returning all happyPlaces in ' + request.POST.get('neighborhood') + ', ' + request.POST.get('city'))
            happyPlaces = HappyPlace.objects.filter(neighborhood=request.POST.get('neighborhood'))
    else:
        happyPlaces = allHappyPlaces

    if request.POST.get('currentTimeOnly') and not request.POST.get('city') == 'defaultCity':
        print('only returning happyHours happening now')
        today = list(DAYSABBREVMAP.keys())[int(list(DAYSINTMAP.values()).index(DAYSINTMAP[str(datetime.utcnow().weekday())]))]
        
        currentDatetime = datetime.utcnow()
        currentDate = currentDatetime.date()
        tomorrowDate = currentDate + timedelta(days=1)
              
        happyHours = [happyHour for happyPlace in happyPlaces for happyHour in happyPlace.happyHours.all()]
        happyHours = [happyHour for happyHour in happyHours if today in happyHour.days]
        
        happyHoursA = [happyHour for happyHour in happyHours if
                      (
                       happyHour.end > happyHour.start
                       and (datetime.combine(currentDate, happyHour.start) - timedelta(hours=happyHour.happyPlace.city.offset) < currentDatetime)
                       and (datetime.combine(currentDate, happyHour.end) - timedelta(hours=happyHour.happyPlace.city.offset) > currentDatetime)
                      )
                      or (str(happyHour.end) == '00:00:02'and str(happyHour.start) == '00:00:01')
                      ] 
        happyHoursB = [happyHour for happyHour in happyHours if
                      (
                       happyHour.end < happyHour.start
                       and (datetime.combine(tomorrowDate, happyHour.end) - timedelta(hours=happyHour.happyPlace.city.offset) > currentDatetime)
                       and (datetime.combine(currentDate, happyHour.start) - timedelta(hours=happyHour.happyPlace.city.offset) < currentDatetime)
                      )
                      or (str(happyHour.end) == '00:00:02'and str(happyHour.start) == '00:00:01')
                      ]
        allHappyHours = happyHoursA + happyHoursB
        
        happyPlaces = list(set(happyHour.happyPlace for happyHour in allHappyHours))
        
    if len(happyPlaces) == 0:
        return HttpResponseRedirect('/error/')
        
    context = {
               'happyPlaces' : happyPlaces
               , 'dayPairs' : DAYS
               , 'today' : intToDayOfWeek((datetime.utcnow() + timedelta(hours=happyPlaces[0].city.offset)).weekday())
               , 'cities' : allCities
               , 'lastSelectedCity' : request.POST.get('city') if request.POST.get('city') is not None else 'defaultCity'
               , 'lastSelectedNeighborhood' : request.POST.get('neighborhood') if request.POST.get('neighborhood') is not None else 'defaultNeighborhood'
               }
    return render(request, 'home.html', context)

def Error(request):
    
    return render(request, 'error.html')

def getNeighborhoodsForCity(request, cityToSearch):
    #reconstruct spaces in search parameter
    cityToSearch = cityToSearch.replace('_', ' ')
    city = City.objects.get(name=cityToSearch)
    happyPlacesInCity = city.happyPlaces.all()
    
    allNeighborhoods = (happyPlace.neighborhood for happyPlace in happyPlacesInCity)
    uniqueNeighborhoods = sorted(set(allNeighborhoods))
    
    return HttpResponse(json.dumps(list(uniqueNeighborhoods)), content_type="application/javascript")

def generateId(objects):
    
    generatedId = uuid4().int % 1000000000

    while objects.filter(id=generatedId):
        generatedId = uuid4().int % 1000000000
    
    print('generated id: ' + str(generatedId))
    return generatedId