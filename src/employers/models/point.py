from geopy import distance, Point


class Point(Point):
    def direct_distance_from(self, other_point):
        return round(distance.distance(self, other_point).meters)

    def __add__(self, other):
        return Point(self.latitude + other.latitude,
                        self.longitude + other.longitude)

    def __sub__(self, other):
        return Point(self.latitude - other.latitude,
                        self.longitude - other.longitude)

    def __mul__(self, scalar):
        return Point(scalar * self.latitude,
                        scalar * self.longitude)

    __rmul__ = __mul__
