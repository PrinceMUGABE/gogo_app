from django.db import models
from django.utils import timezone
from userApp.models import CustomUser
from vehicleApp.models import Vehicle

class Order(models.Model):
    TYPE_CHOICES = [
        ('public', 'Public'),
        ('private', 'Private'),
    ]
    
    PAYMENT_CHOICES = [
        ('successful', 'Successful'),
        ('pending', 'Pending'),
    ]

    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='orders')
    order_name = models.CharField(max_length=255)
    origin = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    vehicle_type = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='orders')
    created_date = models.DateTimeField(default=timezone.now)
    status = models.BooleanField(default=True)
    type = models.CharField(max_length=7, choices=TYPE_CHOICES, default='public')
    payment_status = models.CharField(max_length=10, choices=PAYMENT_CHOICES, default='pending')

    def __str__(self):
        return self.order_name
