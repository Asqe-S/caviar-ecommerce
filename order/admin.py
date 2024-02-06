from django.contrib import admin
from order.models import Order, OrderItems, Review
# Register your models here.
admin.site.register(Order)
admin.site.register(OrderItems)
admin.site.register(Review)
