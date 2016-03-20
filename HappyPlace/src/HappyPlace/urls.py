from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'HappyPlace.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    
    url(r'^submit', 'HappyPlace.site.views.AddHappyPlace', name='add'),
    url(r'^submit/', 'HappyPlace.site.views.AddHappyPlace', name='add'),
    url(r'^', 'HappyPlace.site.views.Home', name='home'),
)
