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

class HappyPlace(models.Model):
    id = models.IntegerField(primary_key=True)

#required fields
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=75)
    city = models.CharField(max_length=50)
    
#optional fields
    site = models.CharField(max_length=50, null=True)
    neighborhood = models.CharField(max_length=50, null=True)
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
    
    happyPlace = models.ForeignKey(HappyPlace)
    
class HappyPlaceForm(ModelForm):
      
    site = forms.CharField(required=False)
    neighborhood = forms.CharField(required=False)
    phone = forms.CharField(required=False)
    cross = forms.CharField(required=False)
    latitude = forms.CharField(required=False)
    longitude = forms.CharField(required=False)
    
    class Meta:
        model = HappyPlace
        fields = ['name', 'city', 'neighborhood', 'address']
        
class HappyHourForm(ModelForm):
    days = forms.MultipleChoiceField(choices=DAYS, widget=forms.CheckboxSelectMultiple())
    happyPlace = forms.ModelChoiceField(queryset=HappyPlace.objects.all().order_by('name'))
    
    class Meta:
        model = HappyHour
        fields = ['start', 'end', 'notes']
