# from django.db import models
# from django.utils import timezone
# from userApp.models import CustomUser
# from vehicleApp.models import Vehicle

# class Freelancer(models.Model):
#     STATUS_CHOICES = [
#         ('pending', 'Pending'),
#         ('approved', 'Approved'),
#     ]
    
#     user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
#     vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
#     vehicle_model = models.CharField(max_length=255)
#     plate_number = models.CharField(max_length=255, unique=True)
    
#     # FileFields to store PDF documents
#     national_id_card = models.FileField(upload_to='documents/national_id/', null=True, blank=True)
#     driving_license = models.FileField(upload_to='documents/driving_license/', null=True, blank=True)
    
#     status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
#     created_date = models.DateTimeField(default=timezone.now)

#     def __str__(self):
#         return self.user.name




from django.db import models
from django.utils import timezone
from userApp.models import CustomUser
from vehicleApp.models import Vehicle
from logistic_company.models import Company  # Assuming you have a Company model

class Freelancer(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('denied', 'Denied'),
    ]
    
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    vehicle_model = models.CharField(max_length=255)
    plate_number = models.CharField(max_length=255, unique=True)
    national_id_card = models.BinaryField(null=True, blank=True)
    driving_license = models.BinaryField(null=True, blank=True)

    
    national_id_card = models.FileField(upload_to='documents/national_id/', null=True, blank=True)
    driving_license = models.FileField(upload_to='documents/driving_license/', null=True, blank=True)
    
    company = models.ForeignKey(Company, on_delete=models.CASCADE)  # New field for selecting a company

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.name} - {self.status}"
