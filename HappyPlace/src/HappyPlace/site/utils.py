import os
import sys
from uuid import uuid4
from django.http.response import HttpResponseBadRequest, HttpResponse
from django.core.serializers import serialize
from HappyPlace.site.models import *
from HappyPlace import settings
from googleplaces import GooglePlaces


GOOGLE_API_KEY = 'AIzaSyDj5RUzdluGjmLNjSVXASlDyvK_LIZ4Qq8'
google_places = GooglePlaces(GOOGLE_API_KEY)

def getPlaceId(request, queryString):
    print("Searching google for..." + queryString)
    
    queryResult = google_places.text_search(queryString)
    data = []
    counter = 0

    googlePlaces = queryResult.places

    while counter < min(5, len(googlePlaces)):
        googleDetails = googlePlaces[counter]
        googleDetails.get_details()
        googleDetails = googleDetails.details

        placeId = googleDetails['place_id']
        latitude = float(googleDetails['geometry']['location']['lat'])
        longitude = float(googleDetails['geometry']['location']['lng'])
        address = googleDetails['formatted_address'].split(',')[0]
        name = googleDetails['name']
    
        price_level = ''
        site = ''
        phone = ''
        
        try:
            price_level = googleDetails['price_level']
        except Exception:
            print(name + ":" + sys.exc_info().__str__())
              
        try:
            site = googleDetails['website']
        except Exception:
            print(name + ":" + sys.exc_info().__str__())
                  
        try:
            phone = googleDetails['formatted_phone_number']
        except Exception:
            print(name + ":" + sys.exc_info().__str__())
         
        data.append({ 'name': name, 'address': address, 'latitude': latitude, 'longitude': longitude , 'price_level': price_level, 'site' : site, 'phone': phone, 'placeId' : placeId })
        
        counter = counter + 1
        
    return HttpResponse(json.dumps(data), content_type="application/javascript")
    
def getNeighborhoodsForCity(request, cityToSearch):
    #reconstruct spaces in search parameter
    cityToSearch = cityToSearch.replace('_', ' ')
    
    neighborhoods = City.objects.all().get(name=cityToSearch).neighborhoods.all()
    
    return HttpResponse(json.dumps(list(map(lambda neighborhood: neighborhood.name, neighborhoods))), content_type="application/javascript")

    
def getHappyPlacesForNeighborhood(request, neighborhoodToSearch):
    neighborhoodToSearch = neighborhoodToSearch.replace('_', ' ')
    
    happyPlaces = Neighborhood.objects.get(name=neighborhoodToSearch).happyPlaces.all()
    return HttpResponse(serialize('json', happyPlaces), content_type="application/javascript")

def getHappyPlace(request, happyPlaceId):
    happyPlace = HappyPlace.objects.get(id=happyPlaceId)
    
    

   
    return HttpResponse(happyPlace.render_to_response(), content_type="application/javascript")

       
def getPhotos(request, location):    
    if location.endswith('all'):
        location = location[:len(location)-3]
        
    folderContents=os.listdir(os.path.join(settings.STATIC_ROOT + 'photos',location))
    photos=list(name for name in folderContents if (os.path.isfile(os.path.join(settings.STATIC_ROOT + 'photos', location + "/" + name))) and name.endswith('jpg'))
    
    return HttpResponse(json.dumps(len(photos)), content_type="application/javascript")

def inflate():
    happyPlaces = HappyPlace.objects.all().filter(googled=False)

    for happyPlace in happyPlaces:
        print(happyPlace.name)
        googleDetails = google_places.text_search(happyPlace.name + ' ' + happyPlace.address + ' ' + happyPlace.city.name).places[0]
        googleDetails.get_details()
        googleDetails = googleDetails.details
     
        happyPlace.latitude = float(googleDetails['geometry']['location']['lat'])
        happyPlace.longitude = float(googleDetails['geometry']['location']['lng'])
        happyPlace.address = googleDetails['formatted_address'].split(',')[0]
        happyPlace.name = googleDetails['name']
        happyPlace.place_id = googleDetails['place_id']
        happyPlace.timeUpdated = datetime.utcnow()
         
        try:
            happyPlace.price_level = googleDetails['price_level']
        except Exception:
            print(happyPlace.name + ":" + sys.exc_info().__str__())
          
        try:
            happyPlace.site = googleDetails['website']
        except Exception:
            print(happyPlace.name + ":" + sys.exc_info().__str__())
              
        try:
            happyPlace.phone = googleDetails['formatted_phone_number']
        except Exception:
            print(happyPlace.name + ":" + sys.exc_info().__str__())
              
        happyPlace.googled = True     
        happyPlace.save()
        
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

def saveNewCity(formData, state):
    cityName = formData['name']
    
    if str(cityName) in list(city.name for city in City.objects.all()):
        return City.objects.get(name=cityName)  
    
    city = City(
            id=generateId(City.objects)
            , name=cityName
            , state=state
            , timeUpdated=datetime.utcnow()
            )
     
    city.save()
    return city

def saveNewHappyPlace(formData, city):
    place_id = formData['place_id']

    if place_id in list(happyPlace.place_id for happyPlace in HappyPlace.objects.all()):
        print('place_id ' + place_id + ' already in DB (' + HappyPlace.objects.get(place_id=place_id).name + ')')
        return HappyPlace.objects.get(place_id=place_id)
    
    def getOrSaveNeighborhood(neighborhoodName):
        print(neighborhoodName)
        if neighborhoodName:
            neighborhood = Neighborhood(
                                        id=generateId(Neighborhood.objects)
                                        , name=neighborhoodName
                                        , city=city
                                        , timeUpdated=datetime.utcnow()
                                        )
            neighborhood.save()
            return neighborhood
        
        else:
            return formData['neighborhood']
        
    happyPlace = HappyPlace(
                            id=generateId(HappyPlace.objects)
                          , name=formData['name']
                          , address=formData['address']
                          , neighborhood=getOrSaveNeighborhood(formData['neighborhoodName'])
                          
                          , cross=None if formData['cross'] == '' else formData['cross']
                          , site=None if formData['site'] == '' else formData['site']
                          , phone=None if formData['phone'] == '' else beautifyPhone(formData['phone'])
                          , latitude=None if formData['latitude'] == '' else formData['latitude']
                          , longitude=None if formData['longitude'] == '' else formData['longitude']
                          
                          , place_id=formData['place_id']
                          
                          , timeUpdated=datetime.utcnow()
                          , active=False
                        )
    
    happyPlace.save()
    return happyPlace

def saveNewHappyHour(formData, happyPlace):
    happyHour = HappyHour(
                    id=generateId(HappyHour.objects)
                    ,notes=formData['notes']
                    ,days=formData['days']
                    ,start=formData['start']
                    ,end=formData['end']
                    ,happyPlace=happyPlace
                    
                    , timeUpdated=datetime.utcnow()
                    )
    
    happyHour.save()
    
    return happyHour

def saveNewFullHappyHour(formData, happyPlace):
    happyHour = HappyHour(
                    id=generateId(HappyHour.objects)
                    ,notes=formData['notes']
                    ,days=formData['days']
                    ,start=formData['start']
                    ,end=formData['end']
                    ,happyPlace=happyPlace
                    ,beer=formData['beer']
                    ,wine_glass=formData['wine_glass']
                    ,wine_bottle=formData['wine_bottle']
                    ,shot_beer=formData['shot_beer']
                    ,well=formData['well']
                    ,display_notes=formData['display_notes']
                    
                    , timeUpdated=datetime.utcnow()
                    )
    
    happyHour.save()
    
    return happyHour

    
def initCityFormView(cityForm, state, context):
    cityForm.fields['city'].queryset = City.objects.filter(state=state).order_by('name')
                
    context['stateId'] = state.id
    
    context['cityForm'] = cityForm
    
    context['displayStateSumbit'] = 'none'
    context['displayCitySumbit'] = 'initial'
    context['displayHappyPlaceSumbit'] = 'none'
    context['displayHappyHourSumbit'] = 'none'
    
def initHappyPlaceFormView(happyPlaceForm, city, context):
    happyPlaceForm.fields['neighborhood'].queryset = Neighborhood.objects.filter(city=city).order_by('name')
    
    context['city'] = city            
    context['cityId'] = city.id
    
    context['happyPlaceForm'] = happyPlaceForm
    
    context['displayStateSumbit'] = 'none'
    context['displayCitySumbit'] = 'none'
    context['displayHappyPlaceSumbit'] = 'initial'
    context['displayHappyHourSumbit'] = 'none'

def initHappyHourFormView(happyHourForm, happyPlace, context):
    context['happyPlace'] = happyPlace
    context['happyPlaceId'] = happyPlace.id
    
    context['happyHourForm'] = happyHourForm
    
    context['displayStateSumbit'] = 'none'
    context['displayCitySumbit'] = 'none'
    context['displayHappyPlaceSumbit'] = 'none'
    context['displayHappyHourSumbit'] = 'initial'