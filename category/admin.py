from django.contrib import admin
from category.models import Genders, Category, SubCategory
# Register your models here.
admin.site.register(Genders)
admin.site.register(Category)
admin.site.register(SubCategory)
