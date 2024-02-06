from django.db import models
from brands.models import Brands
from category.models import Genders, Category, SubCategory


class Size(models.Model):
    size = models.CharField(max_length=20, blank=True)

    class Meta:
        ordering = ['-id']
        verbose_name = 'Size'
        verbose_name_plural = 'Size'

    def __str__(self):
        return self.size


class Products(models.Model):
    name = models.CharField(max_length=255, blank=True)
    description = models.TextField(max_length=2000, blank=True)
    gender = models.ForeignKey(
        Genders, on_delete=models.CASCADE, null=True, blank=True)

    brand = models.ForeignKey(
        Brands, on_delete=models.CASCADE, null=True, blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, null=True, blank=True)

    subcategory = models.ForeignKey(
        SubCategory, on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to='images/products', blank=True)
    active = models.BooleanField(default=False)
    costoftheproduct = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    sellingprice = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    discountprice = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    created = models.DateField(auto_now=True)
    updated = models.DateField(auto_now=True)

    class Meta:
        ordering = ['-id']
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.name

    def off(self):
        if self.sellingprice is not None and self.discountprice is not None and self.sellingprice > 0:
            discount_percentage = (
                (self.sellingprice - self.discountprice) / self.sellingprice) * 100
            return round(discount_percentage)
        else:
            return None


class MultipleImages(models.Model):
    product = models.ForeignKey(
        Products, on_delete=models.CASCADE, null=True, blank=True)
    multipleimages = models.ImageField(
        upload_to='images/multipleimages', blank=True)

    class Meta:
        ordering = ['-id']
        verbose_name = 'Multiple Image'
        verbose_name_plural = 'Multiple Images'

    def __str__(self):
        return self.product.name


class ProductVarient(models.Model):
    product = models.ForeignKey(
        Products, on_delete=models.CASCADE, null=True, blank=True)
    size = models.ForeignKey(
        Size, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'ProductVarient'
        verbose_name_plural = 'ProductVarients'

    def __str__(self):
        return self.product.name
