from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class CustomUser(User):
    image = models.FileField(upload_to='images/profileimages', blank=True)
    phone_number = models.CharField(max_length=30, blank=True)
    verified = models.BooleanField(default=False)
    status = models.BooleanField(default=True)
    wallet = models.FloatField(default=0.00)

    class Meta:
        ordering = ['-id']
        verbose_name = 'Custom User'
        verbose_name_plural = 'Custom Users'

    def __str__(self):
        return self.username
