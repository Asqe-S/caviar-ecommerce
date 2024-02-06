from django.db import models

from security.models import CustomUser

# Create your models here.


class Coupons(models.Model):
    # user=models.ForeignKey(CustomUser,on_delete=models.SET_NULL,
    #     null=True,blank=True,)
    # timeuse=models.CharField(max_length=20,blank=True,null=True)
    # used=models.CharField(max_length=20,blank=True,null=True)

    couponcode = models.CharField(max_length=10, blank=True, null=True)
    off = models.CharField(max_length=10, blank=True, null=True)
    amount = models.CharField(max_length=10, blank=True, null=True)
    validfrom = models.DateField(blank=True, null=True)
    expirydate = models.DateField(blank=True, null=True)

    minimumorderamount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self) -> str:
        return self.couponcode
