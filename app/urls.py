from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('app.views',
    url(r'^$', 'index'),
    url(r'^login$','login'),
    url(r'^seatOrder$', 'seatOrder'),
    url(r'^dishes/(?P<page>\d*)$', 'dishes'),
    url(r'^orderItem$', 'orderItem'),
    url(r'^order$', 'order'),
    url(r'^myOrder$', 'myOrder'),
    url(r'^auth/(?P<authType>\w+)$', 'auth'),
    url(r'^order/complete$','orderComplete'),
    url(r'^profile$', 'profile'),
    url(r'^preorder$', 'preorder'),
    url(r'^exit$', 'exit')
)
