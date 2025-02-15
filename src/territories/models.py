from django.db import models


class Territory(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "territories"

    def __str__(self):
        return self.name
