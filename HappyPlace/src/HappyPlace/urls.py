from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns =  patterns('',
    # Examples:
    # url(r'^$', 'HappyPlace.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    
    #url(r'^happyPlace/(?P<happyPlaceId>\d+)', 'HappyPlace.site.views.HappyPlaceView', name='viewHappyPlace'),
    url(r'^submit/', 'HappyPlace.site.views.Submit', name='submit'),
#     url(r'^submitState/', 'HappyPlace.site.views.SubmitState', name='submitState'),
#     url(r'^submitCityForState/(?P<stateId>[0-9]*)/$', 'HappyPlace.site.views.SubmitCityForState', name='submitCityForState'),
#     url(r'^submitHappyPlaceForCity/(?P<cityId>[0-9]*)/$', 'HappyPlace.site.views.SubmitHappyPlaceForCity', name='submitHappyPlaceForCity'),
#     url(r'^submitHappyHourForHappyPlace/(?P<happyPlaceId>[0-9]*)/$', 'HappyPlace.site.views.SubmitHappyHourForHappyPlace', name='submitHappyHourForHappyPlace'),
    url(r'^error/', 'HappyPlace.site.views.Error', name='error'),
    url(r'^getNeighborhoods/(?P<cityToSearch>\w+)', 'HappyPlace.site.utils.getNeighborhoodsForCity', name='getNeighborhoodsForCity'),
    url(r'^getHappyPlaces/(?P<neighborhoodToSearch>\w+)', 'HappyPlace.site.utils.getHappyPlacesForNeighborhood', name='getHappyPlacesForNeighborhood'),
    
    url(r'^getHappyPlace/(?P<happyPlaceId>\w+)', 'HappyPlace.site.utils.getHappyPlace', name='getHappyPlace'),
    
    url(r'^getPhotos/(?P<location>.+\/.+)', 'HappyPlace.site.utils.getPhotos', name = 'getPhotos'),
    url(r'^getPlaceId/(?P<queryString>.+)', 'HappyPlace.site.utils.getPlaceId', name = 'getPlaceId'),
    url(r'^', 'HappyPlace.site.views.Home', name='home'),    
        
) + staticfiles_urlpatterns()

