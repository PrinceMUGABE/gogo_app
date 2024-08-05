from django.db import models
from django.utils import timezone
from userApp.models import CustomUser

class Company(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
    ]
    
    name = models.CharField(max_length=50, null=False)
    location = models.CharField(max_length=255)
    iso_certificate = models.FileField(upload_to='certificates/iso/', null=True, blank=True)
    rdb_certificate = models.FileField(upload_to='certificates/rdb/', null=True, blank=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.user.name

    def clean(self):
        from django.core.exceptions import ValidationError

        if self.iso_certificate and not self.iso_certificate.name.endswith('.pdf'):
            raise ValidationError('ISO certificate must be a PDF file.')
        if self.rdb_certificate and not self.rdb_certificate.name.endswith('.pdf'):
            raise ValidationError('RDB certificate must be a PDF file.')
