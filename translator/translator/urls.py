from django.conf.urls import patterns, include, url

from . import views

urlpatterns = patterns('',
    # Examples:
    #url(r'^$', 'translator.views.home', name='home'),
    url(r'^$', views.translate, name='translate'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
