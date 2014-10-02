from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('app.views',
    url(r'^$', 'index'),
    url(r'^seatOrder$', 'seatOrder'),
    url(r'^dishes$', 'dishes'),
    url(r'^order$', 'order'),
    url(r'^myOrder$', 'myOrder'),
)
