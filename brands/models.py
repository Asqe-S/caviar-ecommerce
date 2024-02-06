from django.db import models

# Create your models here.


class Brands(models.Model):
    name = models.CharField(max_length=300, blank=True)
    image = models.FileField(upload_to='images/brandimages', blank=True)
    description = models.TextField(max_length=2000, blank=True)
    status = models.BooleanField(default=True)

    class Meta:
        ordering = ['-id']
        verbose_name = 'Brand'
        verbose_name_plural = 'Brands'

    def __str__(self):
        return self.name
