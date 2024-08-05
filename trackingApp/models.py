# trackingApp/models.py

from django.db import models
from vehicleApp.models import Vehicle

class Tracking(models.Model):
    car = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='trackings')
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.car} - {self.created_at}'
