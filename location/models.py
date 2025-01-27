from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings
from authentication.models import *

# Create your models here.

from django.contrib.auth.models import User

class RecipientLocation(models.Model):
    recipient = models.ForeignKey("authentication.Recipient", on_delete=models.CASCADE, related_name="recipient_location")
    latitude = models.FloatField()
    longitude = models.FloatField()
    is_updated = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.recipient.user.username} - ({self.latitude}, {self.longitude})"


class DonorLocation(models.Model):
    donor = models.ForeignKey("authentication.Donor", on_delete=models.CASCADE, related_name="donor_location")
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return f"{self.donor.user.username} - ({self.latitude}, {self.longitude})"
    
    # models.py
from django.db import models
from django.contrib.auth.models import User

class UserLocation(models.Model):
    is_recipient = models.OneToOneField("authentication.Recipient", on_delete=models.CASCADE)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return f"{self.user.username}'s location"


