import json

from django.contrib.gis.db import models
from django.contrib.gis.geos import Point


from chantiers.points import scrape

# in degrees
NEARBY_DISTANCE = 0.001

class ChantierManager(models.GeoManager):
    
    def get_near_line(self, line):
        return self.get_query_set().filter(point__dwithin=(line, NEARBY_DISTANCE))
    
    def wipe_and_scrape(self):
        self.get_query_set().delete()
        scrape_results = scrape.scrape_chantiers()
        for r in scrape_results:
            self.create(
                name=r['name'],
                where=json.dumps(r['where']),
                raw_description=r['raw_description'],
                point=Point(r['point']['lng'], r['point']['lat'])
            )

class Chantier(models.Model):

    name = models.CharField(max_length=500)
    where = models.TextField()
    raw_description = models.TextField()
    
    point = models.PointField()
    
    objects = ChantierManager()
    
    def __unicode__(self):
        return self.name
        
    @property
    def where_list(self):
        return json.loads(self.where)