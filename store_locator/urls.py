from django.conf.urls.defaults import *
from store_locator import views

urlpatterns = patterns('',
    (r'^get_lat_long/$', views.get_lat_long),
    (r'^get_near_locations/$', views.get_near_locations),
    (r'^get_list_locations/$', views.get_list_locations),
)
