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
        print("Received form data")
        form = HappyPlaceForm(request.POST) # A form bound to the POST data

        if form.is_valid():
            print ("Form validated")
            idToInsert = uuid4().int % 1000000000

            while HappyPlace.objects.filter(id=idToInsert):
                idToInsert = uuid4().int % 1000000000
                
            if not form.cleaned_data['site'].startswith('http'):
                form.cleaned_data['site'] = 'http://' + form.cleaned_data['site']
                
            happyPlace = HappyPlace(
                        id=idToInsert
                      , name=form.cleaned_data['name']
                      , address=form.cleaned_data['address']
                      , city=form.cleaned_data['city']
                      , site=form.cleaned_data['site']
                      , neighborhood=form.cleaned_data['neighborhood']
                      , phone=form.cleaned_data['phone']
                      , cross=form.cleaned_data['cross']
                      , latitude=form.cleaned_data['latitude']
                      ,longitude=form.cleaned_data['longitude']
                    )
            
            happyPlace.save()
            print("HappyPlace saved")
            
            return HttpResponseRedirect('/home.html')    

def AddHappyHour(request):
    if request.method == 'POST':
        form = HappyHourForm(request.POST)
        
        if form.is_valid():
            print ("Form validated")
            
            idToInsert = uuid4().int % 1000000000

            while HappyPlace.objects.filter(id=idToInsert):
                idToInsert = uuid4().int % 1000000000
            
            happyHour = HappyHour(
                    id=idToInsert
                    ,notes=form.cleaned_data['notes']
                    ,days=form.cleaned_data['days']
                    ,start=form.cleaned_data['start']
                    ,end=form.cleaned_data['end']
                    ,happyPlace= form.cleaned_data['happyPlace']
                    )
            
            happyHour.save()
            print("HappyHour saved")
        
        return HttpResponseRedirect('/home.html') 
            
def HappyPlaceView(request, happyPlaceId):
    happyPlace = get_object_or_404(HappyPlace ,pk=happyPlaceId)
    
    context = {'happyPlace' : happyPlace}
    return render(request, 'happyPlace.html', context)
        

def Home(request):
    allHappyPlaces = HappyPlace.objects.all()
    if request.method == 'POST':
        if(request.POST.get('neighborhood') == 'all'):
            happyPlaces = HappyPlace.objects.all().filter(city=request.POST.get('city'))
        else:
            happyPlaces = HappyPlace.objects.all().filter(neighborhood=request.POST.get('neighborhood'))
    else:
        happyPlaces = allHappyPlaces
    
    cities = (happyPlace.city for happyPlace in allHappyPlaces)
    
    context = {
               'happyPlaces' : happyPlaces
               , 'dayPairs' : DAYS
               , 'today' : intToDayOfWeek(datetime.now().weekday())
               , 'cities' : set(cities)
               }
    return render(request, 'home.html', context)

def getNeighborhoodsForCity(request, cityToSearch):
    happyPlacesInCity = HappyPlace.objects.all().filter(city=cityToSearch)
    allNeighborhoods = (happyPlace.neighborhood for happyPlace in happyPlacesInCity)
    uniqueNeighborhoods = set(allNeighborhoods)
    
    return HttpResponse(json.dumps(list(uniqueNeighborhoods)), content_type="application/javascript")

        