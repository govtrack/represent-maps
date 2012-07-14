from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin

from maps.models import MapLayer, MapLayerBoundary

class MapLayerAdmin(admin.ModelAdmin):
    list_filter = ('authority',)

admin.site.register(MapLayer, MapLayerAdmin)

class MapLayerBoundaryAdmin(admin.ModelAdmin):
    list_display = ('name', 'maplayer')
    list_display_links = ('name', 'maplayer')
    list_filter = ('maplayer',)
    
    def name(self, obj): return unicode(obj)

admin.site.register(MapLayerBoundary, MapLayerBoundaryAdmin)
