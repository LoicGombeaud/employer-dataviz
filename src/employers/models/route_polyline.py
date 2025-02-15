import polyline

from employers.models import Point


class RoutePolyline():
    def __init__(self, base64):
        self.main_points = list(map(lambda p: Point(p),
                                    polyline.decode(base64)))
