# encoding: utf-8

from django.conf.urls import patterns, include, url

from . import views
from .admin import site

urlpatterns = patterns('',
    # Examples:
    #url(r'^$', 'translator.views.home', name='home'),
    url(r'^$', views.translate, name='translate'),
    url(r'^load_dict/$', views.load_dictionary, name='load_dictionary'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(site.urls)),
)
