from django.conf.urls import patterns, url, include

from maps.views import *

urlpatterns = patterns('',
    url(r'^map/demo/(?P<layer_slug>[\w_-]+)(?:/(?P<boundary_slug>[\w_-]+))?/$', map_demo_page, name='map_demo_page'),
    url(r'^map/tiles/(?P<layer_slug>[\w_-]+)(?:/(?P<boundary_slug>[\w_-]+))?/(?P<tile_zoom>\d+)/(?P<tile_x>\d+)/(?P<tile_y>\d+)\.(?P<format>png|gif|json|jsonp|svg)$', map_tile, name='map_tile'),
)

