from django.db import models
from django.forms import ModelForm
from django import forms
from datetime import datetime, time, timedelta
from HappyPlace.site.templatetags.filters import *
import json

DAYS = (('S','Sunday')
    ,('M','Monday')
    ,('T','Tuesday')
    ,('W','Wednesday')
    ,('R','Thursday')
    ,('F','Friday')
    ,('Y','Saturday'))

ZONES = (('-8','Pacific')
    ,('-7','Mountain')
    ,('-6','Central')
    ,('-5','Eastern'))

class State(models.Model):
    id = models.IntegerField(primary_key=True)
    timeUpdated = models.DateTimeField()
    
    name = models.CharField(max_length=50)
    offset = models.IntegerField(choices=ZONES)
    
    def __str__(self):
        return self.name.__str__()
    
    class Meta:
        ordering = ('name',)
    
class City(models.Model):
    id = models.IntegerField(primary_key=True)
    timeUpdated = models.DateTimeField()
    
    name = models.CharField(max_length=50)
    
    state = models.ForeignKey(State, related_name='state')
        
    def __str__(self):
        return self.name.__str__()
    
    class Meta:
        ordering = ('name',)
        
class HappyPlace(models.Model):
    place_id = models.CharField(max_length=50, primary_key=True)
    id = models.IntegerField(unique=True)
    timeUpdated = models.DateTimeField()

#required fields
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=75)
    neighborhood = models.CharField(max_length=50)
    city = models.ForeignKey(City, related_name='happyPlaces')
    
#optional fields
    cross = models.CharField(max_length=50, null=True)
    site = models.CharField(max_length=75, null=True)
    phone = models.CharField(max_length=50, null=True)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    price_level = models.IntegerField(null=True)
    
    active = models.BooleanField(default=False)
    googled = models.BooleanField(default=False)
    
    def getLatLng(self):
        return {'lat' : self.latitude
                , 'lng' : self.longitude}
    
    latLng = property(getLatLng)
    
    def getMarkerInfo(self):
        
        happyPlaceDetails = list([
                                  self.name
                                  , self.latLng
                                  , self.todaysSpecials
                                  ])
        
        return happyPlaceDetails    
    
    markerInfo = property(getMarkerInfo)
    
    def getTodaysSpecials(self):
        today = intToDayOfWeek((datetime.utcnow() + timedelta(hours=self.city.state.offset)).weekday())
        happyHours = filter(lambda happyHour: today in happyHour.days, self.happyHours.all())
          
        specials = []
        displayNotes = []
          
        for happyHour in happyHours:
            displayNotes = '' if happyHour.display_notes == None else happyHour.display_notes
            specials.append( [formatTime(happyHour.start), formatTime(happyHour.end), displayNotes, [
                                        ['beer', '' if happyHour.beer == None else happyHour.beer]
                                        , ['wine_glass', '' if happyHour.wine_glass == None else happyHour.wine_glass]
                                        , ['wine_bottle', '' if happyHour.wine_bottle == None else happyHour.wine_bottle]
                                        , ['well', '' if happyHour.well == None else happyHour.well]
                                        , ['shot_beer', '' if happyHour.shot_beer == None else happyHour.shot_beer]
                                        ]
                         ])

        return specials
    
    todaysSpecials = property(getTodaysSpecials)
    
    def __str__(self):
        return self.name.__str__()

class HappyHour(models.Model):
    id = models.IntegerField(primary_key=True)
    timeUpdated = models.DateTimeField()
    
    notes = models.CharField(max_length=200)
    days = models.CharField(max_length=100,choices=DAYS)
    start = models.TimeField()
    end = models.TimeField()
    beer = models.CharField(max_length=200, null=True)
    wine_glass = models.CharField(max_length=200, null=True)
    wine_bottle = models.CharField(max_length=200, null=True)
    well = models.CharField(max_length=200, null=True)
    shot_beer = models.CharField(max_length=200, null=True)
    display_notes = models.CharField(max_length=200, null=True)
    
    happyPlace = models.ForeignKey(HappyPlace, to_field='id', related_name='happyHours')



class StateForm(ModelForm):
    state = forms.ModelChoiceField(queryset=State.objects.all().order_by('name'))
        
    class Meta:
        model = State
        fields = ['state']   
    
class CityForm(ModelForm):    
    city = forms.ModelChoiceField(queryset=City.objects.all().order_by('name'), required=False)
    
    name = forms.CharField(max_length=200,required=False)
    
    def is_valid(self):
        if super(CityForm, self).is_valid():
        
            if not (self.cleaned_data['name'] or self.cleaned_data['city']):
                return False
            return True
        
        return False
        
    class Meta:
        model = City
        fields = ['city', 'name']
        
class HappyPlaceForm(ModelForm):      
    place_id = forms.CharField(max_length=200,required=False, error_messages={'unique': "We already have that HappyPlace!"})
    
    name = forms.CharField(max_length=200,required=False)
    address = forms.CharField(max_length=200,required=False)
    neighborhood = forms.CharField(max_length=200,required=False)
    cross = forms.CharField(max_length=200,required=False)
    city = forms.ModelChoiceField(queryset=City.objects.all(), required=False)
    latitude = forms.FloatField(required=False)
    longitude = forms.FloatField(required=False)
    site = forms.CharField(max_length=200,required=False)
    phone = forms.CharField(max_length=200,required=False)
    
    class Meta:
        model = HappyPlace
        fields = ['place_id', 'name', 'address', 'neighborhood', 'cross', 'city', 'latitude', 'longitude', 'site', 'phone']
        
class HappyHourForm(ModelForm):
    
    days = forms.MultipleChoiceField(choices=DAYS, widget=forms.CheckboxSelectMultiple())

    class Meta:
        model = HappyHour
        fields = ['start', 'end', 'notes']
                
class HappyHourAdminForm(ModelForm):    
    
    display_notes = forms.CharField(required=False)
    beer = forms.CharField(required=False)
    well = forms.CharField(required=False)
    cocktail = forms.CharField(required=False)
    wine_glass = forms.CharField(required=False)
    wine_bottle = forms.CharField(required=False)
    shot_beer = forms.CharField(required=False)
    bar = forms.CharField(required=False)
    snacks = forms.CharField(required=False)
    
    days = forms.MultipleChoiceField(choices=DAYS, widget=forms.CheckboxSelectMultiple())

    class Meta:
        model = HappyHour
        fields = ['start', 'end', 'notes']