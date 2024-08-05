from django.db import models
from django.utils import timezone
from orderApp.models import Order


class Payment(models.Model):

    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    ref = models.CharField(max_length=255, default='')
    amount = models.CharField(max_length=255, default='')
    provider = models.CharField(max_length=15, default='')
    status = models.CharField(max_length=10, default='')
    kind = models.CharField(max_length=50, default='')
    created_date = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.order.name