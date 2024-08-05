from django.db import models
from userApp.models import CustomUser

class Vehicle(models.Model):
    type = models.CharField(max_length=50, default='')
    total_weight_to_carry = models.DecimalField(max_digits=10, decimal_places=2)
    price_per_km = models.DecimalField(max_digits=10, decimal_places=2)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='vehicles', null=True, blank=True)

    def __str__(self):
        return f'{self.type} ({self.id})'
