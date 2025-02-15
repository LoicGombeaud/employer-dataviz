import polyline

from employers.models import Point


class RoutePolyline():
    ENRICHMENT_DISTANCE = 3

    def __init__(self, base64):
        self.main_points = list(map(lambda p: Point(p),
                                    polyline.decode(base64)))

    @property
    def enriched_points(self, enrichment_distance=ENRICHMENT_DISTANCE):
        enriched_points = []

        for i in range(len(self.main_points) - 1):
            current_point = self.main_points[i]
            enriched_points.append(current_point)

            next_point = self.main_points[i+1]
            distance_to_next_point = current_point.direct_distance_from(next_point)
            if distance_to_next_point > enrichment_distance:
                num_points_to_add = round(distance_to_next_point / enrichment_distance)
                for j in range(1, num_points_to_add):
                    vector = next_point - current_point
                    step = vector * (j / (num_points_to_add + 1))
                    extra_point = current_point + step
                    enriched_points.append(extra_point)
        return enriched_points
