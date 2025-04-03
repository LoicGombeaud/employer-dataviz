from django.db import models

from employers.models import Address, RoutePolyline
from employers.models import Point
from territories.models import Territory

class Employer(models.Model):
    name = models.CharField(max_length=100)
    territory = models.ForeignKey(Territory, on_delete=models.CASCADE)

    def __str__(self):
        return self.territory.name + " - " + self.name

    @property
    def employee_address_points(self):
        employee_address_points = []
        for site in self.site_set.all():
            employee_address_points.extend(site.employee_address_points)
        return employee_address_points

    @property
    def average_site_address_point(self):
        site_latitudes = list(map(lambda s: s.address.point.latitude,
                                  self.site_set.all()))
        site_longitudes = list(map(lambda s: s.address.point.longitude,
                                   self.site_set.all()))

        average_latitude = sum(site_latitudes) / len(site_latitudes)
        average_longitude = sum(site_longitudes) / len(site_longitudes)

        return Point(average_latitude, average_longitude)

    @property
    def direct_distances(self):
        direct_distances = []
        for site in self.site_set.all():
            direct_distances.extend(site.direct_distances)
        return direct_distances

    @property
    def cycling_distances(self):
        cycling_distances = []
        for site in self.site_set.all():
            cycling_distances.extend(site.cycling_distances)
        return cycling_distances

    #TODO limit to employees within a radius of N km
    @property
    def route_polylines(self):
        route_polylines = []
        for site in self.site_set.all():
            route_polylines.extend(site.route_polylines)
        return route_polylines

    @property
    def route_polyline_segments(self):
        segments = []
        for route_polyline in self.route_polylines:
            segments.extend(RoutePolyline(route_polyline).segments)
        return segments

class Site(models.Model):
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)

    def __str__(self):
        return self.employer.territory.name + " - " + self.employer.name + " - " + self.name

    def update_addresses(self, employee_street_addresses_list):
        self.employee_set.all().delete()
        for street_address in employee_street_addresses_list:
            address, created = Address.objects.get_or_create(street_address=street_address)
            employee, created = Employee.objects.get_or_create(site=self,
                                                               address=address)
            self.employee_set.add(employee)

    @property
    def employee_address_points(self):
        return list(map(lambda e: [e.address.point.latitude,
                                   e.address.point.longitude],
                        self.employee_set.all()))

    @property
    def direct_distances(self):
        return list(map(lambda e: e.direct_distance_from_site,
                        self.employee_set.all()))

    @property
    def cycling_distances(self):
        cycling_distances = []
        for employee in self.employee_set.all():
            cycling_distances.append(employee.cycling_distance_from_site)
        return cycling_distances

    #TODO limit to employees within a radius of N km
    @property
    def route_polylines(self):
        route_polylines = []
        for employee in self.employee_set.filter(direct_distance_from_site__lte=10*1000):
            route_polylines.append(employee.route_polyline_to_site)
            route_polylines.append(employee.route_polyline_from_site)
        return list(filter(lambda rp: rp, route_polylines))

    @property
    def route_polyline_segments(self):
        segments = []
        for route_polyline in self.route_polylines:
            segments.extend(RoutePolyline(route_polyline).segments)
        return segments

class Employee(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    direct_distance_from_site = models.IntegerField(null=True)
    cycling_distance_from_site = models.IntegerField(null=True)
    route_polyline_to_site = models.CharField(max_length=1000,
                                              null=True)
    route_polyline_from_site = models.CharField(max_length=1000,
                                                null=True)

    def __str__(self):
        return str(self.address)

    def save(self, **kwargs):
        self.direct_distance_from_site = self.address.direct_distance_from(self.site.address)
        self.cycling_distance_from_site = self.address.cycling_distance_from(self.site.address)
        self.route_polyline_to_site = self.address.route_polyline_to(self.site.address)
        self.route_polyline_from_site = self.address.route_polyline_from(self.site.address)
        super().save(**kwargs)
