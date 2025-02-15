from django.db import models
from geopy import distance, Point

class Address(models.Model):
    street_address = models.CharField(max_length=100,
                                      primary_key=True)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)

    class Meta:
        verbose_name_plural = "addresses"

    def __str__(self):
        return self.street_address

    @property
    def point(self):
        if self.latitude is None or self.longitude is None:
            self._geocode()
        return Point(self.latitude,
                     self.longitude)

    def _geocode(self):
        #TODO
        #self.latitude = None
        #self.longitude = None
        self.save()

    def direct_distance_from(self, other_address):
        return self.point.direct_distance_from(other_address.point)

class Point(Point):
    def direct_distance_from(self, other_point):
        return round(distance.distance(self, other_point).meters)
