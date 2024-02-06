from django.urls import path
from coupons import views
urlpatterns = [
    path('', views.coupons, name='coupons'),
    path('delete-coupons/', views.deletecoupons, name='deletecoupons')
]
