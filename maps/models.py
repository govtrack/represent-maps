import re

from django.contrib.gis.db import models
from boundaries.models import BoundarySet, Boundary

from appconf import AppConf
from jsonfield import JSONField

class MyAppConf(AppConf):
    MAP_LABEL_FONT = "Ubuntu"

app_settings = MyAppConf()

class MapLayer(models.Model):
    """
    A map layer comprising settings for how to draw a BoundarySet's Boundaries.
    """
    
    boundaryset = models.ForeignKey(BoundarySet, db_index=True)
    
    slug = models.SlugField(max_length=200)

    name = models.CharField(max_length=100, unique=True,
        help_text='A description of the map layer.')
    authority = models.CharField(max_length=256,
        help_text='If the coloring represents measurements or other actual data, this field stores the entity responsible for the coloring data\'s accuracy, e.g. "City of Chicago".')
    last_updated = models.DateField(
        help_text='If the coloring represents measurements or other actual data, the last time this data was updated from its authority (but not necessarily the date it is current as of).')
    source_url = models.URLField(blank=True,
        help_text='If the coloring represents measurements or other actual data, the url this data was found at, if any.')
    notes = models.TextField(blank=True,
        help_text='Notes about the map layer')
    licence_url = models.URLField(blank=True,
        help_text='The URL to the text of the licence the map layer\'s data is distributed under')

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return self.name

class MapLayerBoundary(models.Model):
    """
    Styling information for a Boundary object.
    """
    
    maplayer = models.ForeignKey(MapLayer, db_index=True, related_name="boundaries")
    boundary = models.ForeignKey(Boundary, db_index=True)
    
    color = JSONField(blank=True, null=True,
        help_text='The color to draw this boundary, a (R,G,B) tuple where the values range from 0 to 255, or extended style information as a dict.')
    label_point = models.PointField(
        blank=True, null=True,
        help_text='The location to label this boundary in EPSG:4326 projection, overriding the label_point set on the Boundary itself.')
    metadata = JSONField(blank=True,
        help_text='Additional data for this boundary in this layer.')
    
    class Meta:
        unique_together = (('maplayer', 'boundary'))
        verbose_name_plural = 'Map layer boundaries'

    def __unicode__(self):
        return "#" + unicode(self.boundary)


