from django.db import models

from employers.models import Address, RoutePolyline
from territories.models import Territory

class Employer(models.Model):
    name = models.CharField(max_length=100)
    territory = models.ForeignKey(Territory, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_direct_distances(self):
        direct_distances = []
        for site in self.site_set.all():
            direct_distances.extend(site.get_direct_distances())
        return direct_distances

    def get_cycling_distances(self):
        cycling_distances = []
        for site in self.site_set.all():
            cycling_distances.extend(site.get_cycling_distances())
        return cycling_distances

    def get_route_polyline_points(self):
        route_polyline_points = []
        for site in self.site_set.all():
            route_polyline_points.extend(site.get_route_polyline_points())
        return route_polyline_points

class Site(models.Model):
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)

    def __str__(self):
        return self.employer.name + " - " + self.name

    def update_addresses(self, employee_street_addresses_list):
        self.employee_set.all().delete()
        for street_address in employee_street_addresses_list:
            address, created = Address.objects.get_or_create(street_address=street_address)
            employee, created = Employee.objects.get_or_create(site=self,
                                                               address=address)
            self.employee_set.add(employee)

    def get_direct_distances(self):
        direct_distances = []
        for employee in self.employee_set.all():
            direct_distances.append(employee.get_direct_distance_from_site())
        return direct_distances

    def get_cycling_distances(self):
        cycling_distances = []
        for employee in self.employee_set.all():
            cycling_distances.append(employee.get_cycling_distance_from_site())
        return cycling_distances

    def get_route_polyline_points(self):
        route_polyline_points = []
        for employee in self.employee_set.all():
            route_polyline_points.extend(employee.get_route_polyline_points())
        return route_polyline_points

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

    def get_direct_distance_from_site(self):
        if self.direct_distance_from_site is None:
            self.direct_distance_from_site = self.address.direct_distance_from(self.site.address)
        self.save()
        return self.direct_distance_from_site

    def get_cycling_distance_from_site(self):
        if self.cycling_distance_from_site is None:
            self.cycling_distance_from_site = self.address.cycling_distance_from(self.site.address)
        self.save()
        return self.cycling_distance_from_site

    def get_route_polyline_points(self):
        #TODO get enriched points
        points = []
        points.extend(RoutePolyline(self.get_route_polyline_to_site()).main_points)
        points.extend(RoutePolyline(self.get_route_polyline_from_site()).main_points)
        return list(map(lambda p: [p.latitude, p.longitude],
                        points))

    def get_route_polyline_to_site(self):
        if self.route_polyline_to_site is None:
            self.route_polyline_to_site = self.address.route_polyline_to(self.site.address)
        self.save()
        return self.route_polyline_to_site

    def get_route_polyline_from_site(self):
        if self.route_polyline_from_site is None:
            self.route_polyline_from_site = self.site.address.route_polyline_to(self.address)
        self.save()
        return self.route_polyline_from_site
