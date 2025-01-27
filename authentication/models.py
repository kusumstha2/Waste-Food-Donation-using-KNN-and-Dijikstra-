
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone
from django.core.validators import RegexValidator


class User(AbstractUser):
    is_Donor = models.BooleanField(default=False)
    is_Recipient = models.BooleanField(default=False)
    phone = models.CharField(max_length=10, blank=True)   
    # img = models.ImageField(blank=True, null=True)
    address=models.TextField()
    def __str__(self):
        return self.username
class Donor(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE, related_name="donor")
    phone = models.CharField(max_length=10, blank=True)
    # email = models.EmailField(max_length=255, blank=True)
    
    def __str__(self):
        return self.user.username
    
# @receiver(post_save, sender=settings.AUTH_USER_MODEL)   
# def create_auth_token(sender, instance=None, created=False, **kwargs):
#     if created and instance:
#         Token.objects.create(user=instance)
        
    
class  Recipient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="recipient")
    phone= models.CharField(max_length=10, blank=True)
    # email = models.EmailField(max_length=254, blank=True)
    
    def  __str__(self):
        return self.user.username
    

# OTP Verification Model
class OTPVerification(models.Model):
    email = models.EmailField(unique=True)
    otp = models.CharField(max_length=6)
    otp_created_at = models.DateTimeField(default=timezone.now)

    def is_expired(self):
        expiration_time = self.otp_created_at + timezone.timedelta(minutes=10)
        return timezone.now() > expiration_time

    def __str__(self):
        return f"OTP for {self.email}"
