from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [ patterns('',
    # Examples:
    # url(r'^$', 'HappyPlace.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    
    url(r'^happyPlace/(?P<happyPlaceId>\d+)', 'HappyPlace.site.views.HappyPlaceView', name='viewHappyPlace'),
    url(r'^submit', 'HappyPlace.site.views.AddHappyPlace', name='add'),
    url(r'^submit/', 'HappyPlace.site.views.AddHappyPlace', name='add'),
    url(r'^', 'HappyPlace.site.views.Home', name='home'),
) ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

