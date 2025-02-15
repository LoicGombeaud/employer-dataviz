from django.db import models
from django.contrib.auth.models import User

from employers.models import Employer, Territory

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
