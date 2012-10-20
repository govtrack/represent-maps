#coding: utf8

import logging
log = logging.getLogger(__name__)
from optparse import make_option
import os, os.path
import sys
import random

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import connections, DEFAULT_DB_ALIAS, transaction
import django.db.utils

from boundaries.models import BoundarySet, Boundary
from maps.models import MapLayer, MapLayerBoundary

class Command(BaseCommand):
    help = 'Create a new MapLayer for a BoundarySet.'
    option_list = BaseCommand.option_list + (
        make_option('-c', '--color', action='store_true', dest='color',
            default=False, help='Automatically set colors to the boundaries.'),
    )

    def handle(self, *args, **options):
        if len(args) == 0 or len(args) > 3:
            print "Usage: manage.py create-layer boundarysetslug [maplayerslug [colorfunc]]"
            return
        
        bs = args[0]
        ml = bs
        colorfunc = None
        if len(args) >= 2: ml = args[1]
        if len(args) >= 3: colorfunc = args[2]
        
        bsqs = BoundarySet.objects.filter(slug=bs)
        if len(bsqs) == 0:
            print "No BoundarySet with that slug."
            return
        bs = bsqs[0]
        
        if colorfunc:
            if options["color"]:
                print "Cannot specify both -c and a colorfunc."
                return
            if not "." in colorfunc:
                print "colorfunc must be a Django-style module.method name."
                return
            module, method = colorfunc.rsplit(".", 1)
            __import__(module)
            module = sys.modules[module]
            if not hasattr(module, method):
                print "method %s not found in module %s." % (method, module)
                return
            colorfunc = getattr(module, method)
        
        MapLayer.objects.filter(slug=ml).delete()
        
        ml = MapLayer.objects.create(
            slug=ml,
            boundaryset=bs,
            name=bs.name,
            last_updated=bs.last_updated)
        
        # Don't fetch actual instances because they are large and plentiful
        # and we don't want to load them in memory.
        #for bdry in bs.boundaries.values_list('id', flat=True):
        for bdry in bs.boundaries.only("slug", "external_id", "metadata").iterator():
            create_args = { "maplayer": ml, "boundary": bdry } # was _id
            if colorfunc:
                create_args["color"] = colorfunc(bdry)
            mlb = MapLayerBoundary.objects.create(**create_args)

        if options["color"]:
            self.assign_colors(ml)

    @staticmethod
    def assign_colors(layer):
        # For each boundary in the layer, assign a color such that it does not have the same
        # color as any other boundary it touches. Use the main colors from the Brewer spectrum,
        # based on http://colorbrewer2.org. This is done in a pretty dumb way: loop through
        # each boundary, query for each boundary it touches, look for a remaining color, and
        # then continue. In principle only four colors should be needed (the Four Color Theorem),
        # but finding a coloring that only uses four colors is algorithmically difficult. In practice,
        # around 8 is enough, and if we get stuck we just reuse a neighboring color --- oh well.
        
        color_choices = [ (44,162,95), (136,86,167), (67,162,202), (255, 237, 160), (240,59,32), (153,216,201), (158,188,218), (253,187,132), (166,189,219), (201,148,199) ]
        
        # Reset colors.
        layer.boundaries.all().update(color=None)
        
        # Loop over all boundaries in layer. Fetch IDs first so that we don't load whole instance
        # data for the entire layer into memory.
        for bdry in layer.boundaries.values_list('id', flat=True):
            bdry = MapLayerBoundary.objects.get(id=bdry)
            used_colors = set()
            
            # What shapes are neighbors? 'Touches' is the right operator, but to be flexible
            # we use intersects, which will allow some overlap for poorly defined geometry.
            # Sometimes __intersects throws an error ("django.db.utils.DatabaseError: GEOS
            # intersects() threw an error!") and we'll just try to pass over those.
            try:
                neighbors = layer.boundaryset.boundaries.filter(shape__intersects=bdry.boundary.shape)
                for b2 in layer.boundaries.filter(boundary__in=neighbors)\
                  .exclude(color=None).only("color"):
                    used_colors.add(tuple(b2.color))
            except django.db.utils.DatabaseError as e:
                print '%s had a problem looking for intersecting boundaries...' % bdry.boundary.slug
                bdry.color = random.choice(color_choices)
                bdry.save()
                continue
            
            # Choose the first available color. We prefer not to randomize so that a) this process
            # is relatively stable from run to run, and b) we can prioritize the colors we'd rather
            # use. The colors above are roughly from stronger to weaker.
            for c in color_choices:
                if c not in used_colors:
                    bdry.color = c
                    break
            else:
                # We ran out of colors. Just choose one at random.
                bdry.color = random.choice(color_choices)
            bdry.save()


