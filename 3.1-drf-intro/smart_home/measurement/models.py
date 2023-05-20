from django.db import models


class Sensor(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Reading(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.PROTECT, related_name='measurements')
    temperature = models.DecimalField(max_digits=6, decimal_places=2)
    created_at = models.DateTimeField(auto_now=True)
    photo = models.ImageField(null=True)

    def __str__(self):
        return f'{self.sensor.name}:{self.created_at}'