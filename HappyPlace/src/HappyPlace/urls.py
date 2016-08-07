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
    
    url(r'^getNeighborhoods/(?P<cityToSearch>\w+)', 'HappyPlace.site.views.getNeighborhoodsForCity', name='getNeighborhoodsForCity'),
    url(r'^happyPlace/(?P<happyPlaceId>\d+)', 'HappyPlace.site.views.HappyPlaceView', name='viewHappyPlace'),
    url(r'^submit/', 'HappyPlace.site.views.SubmissionFormsView', name='submit'),
    url(r'^submit$', 'HappyPlace.site.views.SubmissionFormsView', name='submit'),
    url(r'^submitCity/', 'HappyPlace.site.views.AddCity', name='addCity'),
    url(r'^submitHappyHour/', 'HappyPlace.site.views.AddHappyHour', name='addHappyHour'),
    url(r'^submitHappyPlace/', 'HappyPlace.site.views.AddHappyPlace', name='addHappyPlace'),
    url(r'^error/', 'HappyPlace.site.views.Error', name='error'),
    url(r'^', 'HappyPlace.site.views.Home', name='splash'),    
        
) + staticfiles_urlpatterns()

