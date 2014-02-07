from django.conf.urls import patterns, include, url
from django.contrib.auth.forms import UserCreationForm

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'testApp.views.index', name='home'),
    url(r'^view2$', 'testApp.views.view2', name='secondView'),
    url(r'^login/$', 'django.contrib.auth.views.login'),
    url(r'^logout/$', 'testApp.views.logout_view'),
    url(r'^register/$', 'testApp.views.register'),
    url(r'^profile/(?P<user_id>\d+)$', 'testApp.views.profile'),
    url(r'^oauth/redirect/$', 'testApp.views.handle_oauth'),
    url(r'^oauth/start/$', 'testApp.views.link_oauth'),
    
    # url(r'^lab1/', include('lab1.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
