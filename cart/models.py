from django.db import models
from product.models import ProductVarient
from security.models import CustomUser

# Create your models here.


class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductVarient, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    total = models.DecimalField(
        null=True, blank=True, max_digits=10, decimal_places=2)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.user.username

    def totalprice(self):
        if self.product.quantity > 0:
            return self.total
        else:
            return 0
