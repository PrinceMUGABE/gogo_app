# orderApplicationApp/models.py
from django.db import models
from django.utils import timezone
from orderApp.models import Order
from freelancerApp.models import Freelancer

class OrderApplication(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('delivered', 'Delivered'),
        ('failed', 'Failed'),
    ]

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    freelancer = models.ForeignKey(Freelancer, on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"OrderApplication {self.id} - {self.order.order_name} by {self.freelancer.user.name}"

    def save(self, *args, **kwargs):
        if not self.id:
            self.order.status = False  # Set order to unavailable when a new application is created
            self.order.save()
        super(OrderApplication, self).save(*args, **kwargs)
