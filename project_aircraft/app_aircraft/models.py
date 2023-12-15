from django.db import models
from datetime import timedelta
from django.utils import timezone
from django.core.exceptions import ValidationError

# Create your models here.

#Aircraft Model
class Aircraft(models.Model):
    serial_number = models.CharField(max_length=100, unique=True, null=False, blank=False)
    manufacturer = models.CharField(max_length=100)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.serial_number

class Flight(models.Model):
    aircraft = models.ForeignKey(Aircraft, on_delete=models.CASCADE)
    departure_airport = models.CharField(max_length=4)
    arrival_airport = models.CharField(max_length=4)
    departure_datetime = models.DateTimeField()
    arrival_datetime = models.DateTimeField()
    duration = models.DurationField(null=True, blank=True)
