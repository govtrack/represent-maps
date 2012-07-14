# Represent API: Maps

This app generates colorful map layers for Google Maps API or OpenLayers, and is based on the [represent-boundaries](https://github.com/rhymeswithcycle/represent-boundaries) app by OpenNorth, a fork of a similar project by the Chicago Tribune named [django-boundaryservice](http://github.com/newsapps/django-boundaryservice).

The [boundaries_us](https://github.com/tauberer/boundaries_us) repository provides a full deployment and example data for the United States.

When you use this app, you first load in geographic boundary data from shapefiles using the [represent-boundaries](https://github.com/rhymeswithcycle/represent-boundaries) management command loadshapefiles. That creates a BoundarySet (which has a slug like congressional-districts) and in that set a Boundary record for each district (a polygon or set of polygons).

Then you create MapLayer records. A MapLayer is a particular set of styling options for a BoundarySet. In a MapLayer, you assign a color to each Boundary. That information is stored in a MapLayerBoundary record (which has a foreign key to the Boundary it corresponds to).

The output are map tile image that would typically be used to overlay on street maps.

The map tiles are not cached within the app. That's your responsibility. 
   
## Installation

Besides the dependencies for represent-boundaries, you'll need pycairo2. It's available in Ubuntu 12.04. Your mileage may vary in other cases:

    apt-get install python-cairo # (there's no PIP for Python 2?)
    
Add `maps` to INSTALLED_APPS in your settings.py.

Run `python manage.py syncdb` to create the new tables.

Place in your urls.py:

   (r'', include('maps.urls')),

## Creating map layers

First load in the boundaries data:

   python manage.py loadshapefiles --only [your-boundary-set-slug]

Then create a new map layer with automatically chosen colors for each boundary:

   python manage.py create-layer -c [your-boundary-set-slug]

A new layer is created with the same slug as the BoundarySet. The -c option assigns colors to each Boundary.
   
Then launch the server and view a map example at:

   /map/demo/[your-boundary-set-slug]/

For an example with real data, see [boundaries_us](https://github.com/tauberer/boundaries_us).

