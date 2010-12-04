from django.contrib.gis import admin

from chantiers.points.models import *

class ChantierAdmin(admin.OSMGeoAdmin):
    search_fields = ['name']

admin.site.register(Chantier, ChantierAdmin)