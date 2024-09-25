<<<<<<< HEAD
=======
# orders/models.py

>>>>>>> 369378f (first commit)
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
<<<<<<< HEAD
=======

class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payments')  # Link to Order model
    ref = models.CharField(max_length=255, unique=True)  # Unique reference ID for the payment
    status = models.CharField(max_length=50)  # Status of the payment (e.g., pending, completed)
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Payment amount
    provider = models.CharField(max_length=50)  # Payment provider (e.g., MTN)
    kind = models.CharField(max_length=50)  # Type of payment (e.g., CASHIN)
    created_at = models.DateTimeField(default=timezone.now)  # Timestamp when the payment was created

    def __str__(self):
        return f"Payment {self.ref} for Order {self.order.id}"
>>>>>>> 369378f (first commit)
