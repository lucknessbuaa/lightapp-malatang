from django.conf.urls import patterns, include, url
import views

urlpatterns = patterns('backend.views',
    url(r'^$', 'index'),
    url(r'^login$', 'login'),
    url(r'^exit$', 'exit')
)

urlpatterns = urlpatterns + patterns('backend.takeout_views',
    url(r'^takeout$', 'takeout')
)

urlpatterns = urlpatterns + patterns('backend.dishes_views',
    url(r'^dishes$', 'dishes'),
    url(r'^dishes/(?P<id>\d+)$', 'edit_dishes'),
    url(r'^dishes/add$', 'add_dishes'),
    url(r'^dishes/delete$', 'delete_dishes')
)

urlpatterns = urlpatterns + patterns('backend.preorder_views',
    url(r'^preorder$', 'preorder')
)

urlpatterns = urlpatterns + patterns('backend.user_views',
    url(r'^user$', 'user')
)
