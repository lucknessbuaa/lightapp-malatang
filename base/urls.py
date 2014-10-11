from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic.base import RedirectView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'base.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^oauth/', include('social_auth.urls')),
    url(r'^$',RedirectView.as_view(url='app/')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^app/', include('app.urls')),
)
