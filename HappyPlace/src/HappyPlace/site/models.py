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
    notes = models.CharField(max_length=200)
    days = models.CharField(max_length=50,choices=DAYS)
    start = models.TimeField()
    end = models.TimeField()
    
#optional fields
    site = models.CharField(max_length=50, null=True)
    neighborhood = models.CharField(max_length=50, null=True)
    phone = models.CharField(max_length=50, null=True)
    cross = models.CharField(max_length=50, null=True)
        
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.name.__str__()

class HappyPlaceForm(ModelForm):
    days = forms.MultipleChoiceField(choices=DAYS, widget=forms.CheckboxSelectMultiple())
    start = forms.TimeField(widget=widgets.AdminTimeWidget())
    end = forms.TimeField(widget=widgets.AdminTimeWidget())
    
    site = forms.CharField(required=False)
    neighborhood = forms.CharField(required=False)
    phone = forms.CharField(required=False)
    cross = forms.CharField(required=False)
    
    class Meta:
        model = HappyPlace
        fields = ['name', 'city', 'neighborhood', 'address', 'cross', 'phone', 'site',  'start', 'end', 'notes']