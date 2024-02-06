from django.db import models
from product.models import Products
from security.models import CustomUser

# Create your models here.


class Wishlist(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-id']
        verbose_name = 'Whishlist'
        verbose_name_plural = 'Whishlist'

    def __str__(self):
        return self.user.username
