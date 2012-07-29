from django.conf.urls.defaults import patterns, include, url

from maps.views import *

urlpatterns = patterns('',
    url(r'^map/demo/(?P<layer_slug>[\w_-]+)(?:/(?P<boundary_slug>[\w_-]+))?/$', map_demo_page, name='map_demo_page'),
    url(r'^map/tiles/(?P<layer_slug>[\w_-]+)(?:/(?P<boundary_slug>[\w_-]+))?/(?P<tile_zoom>\d+)/(?P<tile_x>\d+)/(?P<tile_y>\d+)\.(?P<format>png|json|jsonp|svg)$', map_tile, name='map_tile'),
)

