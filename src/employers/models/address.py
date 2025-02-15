import openrouteservice
import os
from django.db import models

from employers.models import Point


ors_client = openrouteservice.Client(key=os.environ["ORS_API_KEY"])

class Address(models.Model):
    street_address = models.CharField(max_length=100,
                                      primary_key=True)
    latitude = models.FloatField(null=True,
                                 blank=True)
    longitude = models.FloatField(null=True,
                                  blank=True)

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
        pelias_result = ors_client.pelias_search(text=self.street_address)
        coordinates = pelias_result["features"][0]["geometry"]["coordinates"]
        self.latitude = coordinates[1]
        self.longitude = coordinates[0]
        self.save()

    def direct_distance_from(self, other_address):
        return self.point.direct_distance_from(other_address.point)

    def cycling_distance_from(self, other_address):
        directions = ors_client.directions([[self.point.longitude, self.point.latitude],
                                            [other_address.point.longitude, other_address.point.latitude]],
                                           profile="cycling-regular")
        return directions["routes"][0]["summary"]["distance"]

    def route_polyline_to(self, other_address):
        directions = ors_client.directions([[self.longitude, self.latitude],
                                            [other_address.longitude, other_address.latitude]],
                                           profile="cycling-regular")
        return directions["routes"][0]["geometry"]
