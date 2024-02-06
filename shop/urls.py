from django.urls import path
from shop import views
urlpatterns = [
    path('', views.offers, name='offers'),
    path('shopby/<str:type>/<str:name>/', views.shop, name='shop'),

]
