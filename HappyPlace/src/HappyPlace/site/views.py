import os
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from HappyPlace.site.models import *
from uuid import uuid4
from django.http.response import HttpResponseBadRequest, HttpResponse

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
                      , notes=form.cleaned_data['notes']
                      , days=form.cleaned_data['days']
                      , start=form.cleaned_data['start']
                      , end=form.cleaned_data['end']
                      , site=form.cleaned_data['site']
                      , neighborhood=form.cleaned_data['neighborhood']
                      , phone=form.cleaned_data['phone']
                      , cross=form.cleaned_data['cross']
                    )
            
            happyPlace.save()
            print("HappyPlace saved")
            
            return HttpResponseRedirect('/home.html')    

    else:
        form = HappyPlaceForm()
    
    context = {'form' : form}        
    return render(request, 'addHappyPlace.html', context)
    
def HappyPlaceView(request, happyPlaceId):
    happyPlace = get_object_or_404(HappyPlace ,pk=happyPlaceId)
    
    context = {'happyPlace' : happyPlace}
    return render(request, 'happyPlace.html', context)
        

def Home(request):
    context = {
               'happyPlaces' : HappyPlace.objects.all()
               , 'dayPairs' : DAYS
               }
    return render(request, 'home.html', context)