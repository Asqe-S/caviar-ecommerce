from django.db import models

from security.models import CustomUser

# Create your models here.


class Address(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True)
    name = models.CharField(max_length=50, blank=True)
    type_of_address = models.CharField(max_length=50, blank=True)
    phone_number = models.CharField(max_length=50, blank=True)
    alternate_phone_number = models.CharField(max_length=50, blank=True)
    pincode = models.CharField(max_length=50, blank=True)
    city = models.CharField(max_length=255, blank=True)
    state = models.CharField(max_length=255, blank=True)
    house = models.TextField(max_length=2000, blank=True)
    road = models.TextField(max_length=2000, blank=True)

    class Meta:
        ordering = ['id']
        verbose_name = 'Address'
        verbose_name_plural = 'Address'

    def __str__(self):
        return self.user.username
