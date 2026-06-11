from django.db import models

# Create your models here.
from django.utils import timezone
from datetime import timedelta

OTP_EXPIRY_IN_MINUTES = 10

class EmailOTP(models.Model):
    email = models.EmailField()
    # 6 digit otp
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(minutes = OTP_EXPIRY_IN_MINUTES)
    
    def __str__(self):
        return f'{self.email} - {self.otp}'