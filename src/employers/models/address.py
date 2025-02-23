import openrouteservice
import os
from django.db import models
from geopy import BANFrance

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

    def save(self, **kwargs):
        if self.latitude is None or self.longitude is None:
            location = BANFrance().geocode(self.street_address)
            self.latitude = location.latitude
            self.longitude = location.longitude
        super().save(**kwargs)

    @property
    def point(self):
        return Point(self.latitude,
                     self.longitude)

    def direct_distance_from(self, other_address):
        return self.point.direct_distance_from(other_address.point)

    def cycling_distance_from(self, other_address):
        try:
            directions = ors_client.directions([[self.point.longitude,
                                                 self.point.latitude],
                                                [other_address.point.longitude,
                                                 other_address.point.latitude]],
                                               profile="cycling-regular")
            return directions["routes"][0]["summary"]["distance"]
        except Exception as e:
            print(f"Error getting cycling distance from {self} to {other_address}")
            #TODO handle error better
            return 100*1000

    def route_polyline_to(self, other_address):
        try:
            directions = ors_client.directions([[self.longitude, self.latitude],
                                                [other_address.longitude, other_address.latitude]],
                                               profile="cycling-regular")
            return directions["routes"][0]["geometry"]
        except Exception as e:
            print(f"Error getting directions from {self} to {other_address}")

    def route_polyline_from(self, other_address):
        return other_address.route_polyline_to(self)
