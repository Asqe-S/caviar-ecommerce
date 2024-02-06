from django.db import models
from product.models import ProductVarient, Products

from security.models import CustomUser
from userdetails.models import Address


class Order(models.Model):

    user = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, blank=True, null=True
    )
    address = models.ForeignKey(
        Address, on_delete=models.SET_NULL, blank=True, null=True)
    order_number = models.CharField(max_length=100, blank=True)
    order_total = models.FloatField()
    payment_id = models.CharField(max_length=200)
    payment_method = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    wallet_amount = models.FloatField(default=0, blank=True, null=True)
    deliverycharge = models.FloatField(default=0, blank=True, null=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.user.username + " " + self.order_number


class OrderItems(models.Model):
    STATUS = (
        ("Order Processing", "Order Processing"),
        ("Confirmed", "Confirmed"),
        ("Shipped", "Shipped"),
        ("Delivered", "Delivered"),
    )
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductVarient, on_delete=models.CASCADE)
    quantity = models.IntegerField(blank=True)
    unitprice = models.FloatField(blank=True, null=True)
    product_price = models.FloatField(blank=True)
    profit = models.FloatField(blank=True, null=True)
    reason = models.TextField(max_length=2000, blank=True)
    is_cancelled = models.BooleanField(default=False)
    returndate = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        max_length=20, choices=STATUS, default="Order Processing")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.product.product.name


class Review(models.Model):
    user = models.CharField(max_length=255, blank=True, null=True)
    product = models.ForeignKey(
        Products, on_delete=models.CASCADE, null=True, blank=True)
    review = models.TextField(max_length=3000, blank=True)
    orderitems = models.ForeignKey(
        OrderItems, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.user+" "+self.product.name
