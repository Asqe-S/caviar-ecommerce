from django.db import models

# Create your models here.


class Genders(models.Model):
    name = models.CharField(max_length=300)
    status = models.BooleanField(default=True)

    class Meta:
        ordering = ['-id']

        verbose_name = 'Gender'
        verbose_name_plural = 'Gender'

    def __str__(self):
        return self.name


class Category(models.Model):
    gender = models.ForeignKey(
        Genders, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=300)
    status = models.BooleanField(default=True)

    class Meta:
        ordering = ['-id']
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.gender.name + ' ' + self.name


class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=300)
    status = models.BooleanField(default=True)

    class Meta:
        ordering = ['-id']

        verbose_name = ' Sub Category'
        verbose_name_plural = 'Sub Categories'

    def __str__(self):
        return self.category.gender.name + ' ' + self.category.name + ' ' + self.name
