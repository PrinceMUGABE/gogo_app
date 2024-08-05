from django.db import models
from django.utils import timezone
from userApp.models import CustomUser
from vehicleApp.models import Vehicle
from orderApp.models import Order

class DiscountOrder(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='discount')
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    price_per_km = models.DecimalField(max_digits=10, decimal_places=2)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'DiscountOrder {self.id} - {self.order.order_name}'
