from django.db import models


class Address(models.Model):
    street_address = models.CharField(max_length=100,
                                      primary_key=True)

    class Meta:
        verbose_name_plural = "addresses"

    def __str__(self):
        return self.street_address
