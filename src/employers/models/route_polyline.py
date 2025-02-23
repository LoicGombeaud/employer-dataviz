import polyline
from django.conf import settings

from employers.models import Point


class RoutePolyline():

    def __init__(self, base64):
        self.main_points = list(map(lambda p: Point(p),
                                    polyline.decode(base64)))

    @property
    def segments(self):
        segments = []
        for i in range(len(self.main_points) - 1):
            segments.append([self.main_points[i].lat_lng,
                             self.main_points[i+1].lat_lng])
        return segments
