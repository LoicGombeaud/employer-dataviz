from django.db import models
from django.contrib.auth.models import User


class Territory(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "territories"

    def __str__(self):
        return self.name

class Employer(models.Model):
    name = models.CharField(max_length=100)
    territory = models.ForeignKey(Territory, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_distance_stats(self):
        return "TODO"

    def get_map_data(self):
        return "TODO"

class EmployerLiaison(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.employer) + " - " + str(self.user)

class TerritoryLiaison(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    territory = models.ForeignKey(Territory, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.territory) + " - " + str(self.user)

class Address(models.Model):
    street_address = models.CharField(max_length=100,
                                      primary_key=True)

    class Meta:
        verbose_name_plural = "addresses"

    def __str__(self):
        return self.street_address

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

class Employee(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.address)
