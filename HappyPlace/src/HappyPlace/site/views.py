import os
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from HappyPlace.site.models import *
from uuid import uuid4
from django.http.response import HttpResponseBadRequest, HttpResponse
from datetime import datetime
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
                    print('appending http...')
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
            
# def HappyPlaceView(request, happyPlaceId):
#     happyPlace = get_object_or_404(HappyPlace ,pk=happyPlaceId)
#     
#     context = {'happyPlace' : happyPlace}
#     return render(request, 'happyPlace.html', context)
        

def Home(request):
    allHappyPlaces = HappyPlace.objects.all()
    allCities = sorted(set(happyPlace.city for happyPlace in allHappyPlaces))
    
    if request.method == 'POST':
        print('received POST on home view')
        if request.POST.get('city') == "Z":
            print('no city selected, returning all happyPlaces')
            happyPlaces = allHappyPlaces           
        elif request.POST.get('neighborhood') == 'all':
            print('no neighborhood selected, returning all happyPlaces for ' + request.POST.get('city'))
            happyPlaces = HappyPlace.objects.all().filter(city=request.POST.get('city'))
        else:
            print('returning all happyPlaces in ' + request.POST.get('neighborhood') + ', ' + request.POST.get('city'))
            happyPlaces = HappyPlace.objects.all().filter(neighborhood=request.POST.get('neighborhood'))
    else:
        happyPlaces = allHappyPlaces
    
    context = {
               'happyPlaces' : happyPlaces
               , 'dayPairs' : DAYS
               , 'today' : intToDayOfWeek(datetime.now().weekday())
               , 'cities' : allCities
               }
    return render(request, 'home.html', context)

def getNeighborhoodsForCity(request, cityToSearch):
    happyPlacesInCity = HappyPlace.objects.all().filter(city=cityToSearch)
    allNeighborhoods = (happyPlace.neighborhood for happyPlace in happyPlacesInCity)
    uniqueNeighborhoods = sorted(set(allNeighborhoods))
    
    return HttpResponse(json.dumps(list(uniqueNeighborhoods)), content_type="application/javascript")

def generateId(objects):
    
    generatedId = uuid4().int % 1000000000

    while objects.filter(id=generatedId):
        generatedId = uuid4().int % 1000000000
    
    print('generated id: ' + str(generatedId))
    return generatedId