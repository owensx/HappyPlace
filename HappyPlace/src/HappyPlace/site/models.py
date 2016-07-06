from django.db import models
from django.forms import ModelForm
from django import forms
from django.contrib.admin import widgets

DAYS = (('S','Sunday')
    ,('M','Monday')
    ,('T','Tuesday')
    ,('W','Wednesday')
    ,('R','Thursday')
    ,('F','Friday')
    ,('Y','Saturday'))

class City(models.Model):
    id = models.IntegerField(primary_key=True)
    
    name = models.CharField(max_length=50)
    offset = models.IntegerField()
    
    def __str__(self):
        return self.name.__str__()
    
    class Meta:
        ordering = ('name',)
        
class HappyPlace(models.Model):
    id = models.IntegerField(primary_key=True)

#required fields
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=75)
    neighborhood = models.CharField(max_length=50)
    city = models.ForeignKey(City, related_name='happyPlaces')
    
#optional fields
    site = models.CharField(max_length=50, null=True)
    phone = models.CharField(max_length=50, null=True)
    cross = models.CharField(max_length=50, null=True)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.name.__str__()

class HappyHour(models.Model):
    id = models.IntegerField(primary_key=True)
    
    notes = models.CharField(max_length=200)
    days = models.CharField(max_length=100,choices=DAYS)
    start = models.TimeField()
    end = models.TimeField()
    
    happyPlace = models.ForeignKey(HappyPlace, related_name='happyHours')

class CityForm(ModelForm):
    
    class Meta:
        model = City
        fields = ['name', 'offset']
        
class HappyPlaceForm(ModelForm):
      
    site = forms.CharField(required=False)
    phone = forms.CharField(required=False)
    cross = forms.CharField(required=False)
    latitude = forms.CharField(required=False)
    longitude = forms.CharField(required=False)
    
    class Meta:
        model = HappyPlace
        fields = ['name', 'city', 'address', 'neighborhood']
        
class HappyHourForm(ModelForm):
    happyPlace = forms.ModelChoiceField(queryset=HappyPlace.objects.all().order_by('name'))
    days = forms.MultipleChoiceField(choices=DAYS, widget=forms.CheckboxSelectMultiple())
    
    class Meta:
        model = HappyHour
        fields = ['start', 'end', 'notes']
