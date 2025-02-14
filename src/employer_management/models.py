from django.db import models

class Employer(models.Model):
    name = models.CharField(max_length=100)

class Address(models.Model):
    street_address = models.CharField(max_length=100)

class EmployerSite(models.Model):
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)

class Employee(models.Model):
    employer_site = models.ForeignKey(EmployerSite, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
