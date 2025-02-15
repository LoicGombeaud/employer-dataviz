from geopy import distance, Point


class Point(Point):
    def direct_distance_from(self, other_point):
        return round(distance.distance(self, other_point).meters)
