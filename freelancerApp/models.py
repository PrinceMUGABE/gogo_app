from django.db import models
from django.utils import timezone
from userApp.models import CustomUser
from vehicleApp.models import Vehicle

class Freelancer(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
    ]
    
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    vehicle_model = models.CharField(max_length=255)
    plate_number = models.CharField(max_length=255, unique=True)
    national_id_card = models.BinaryField(null=True, blank=True)
    driving_license = models.BinaryField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.user.name
