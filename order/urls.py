from django.urls import path
from order import views
urlpatterns = [
    path('', views.order, name='order'),
    path('checkout/', views.checkout, name="checkout"),
    path('confirm/', views.confirm, name="confirm"),
    path('success/', views.success, name='success'),


    path('order-details/<int:id>/',
         views.userordersdetails, name='userordersdetails'),
    path('cancelorder', views.cancelorder, name='cancelorder'),

    path('return-product/', views.returnproduct, name='returnproduct'),



    path('proceed-to-pay/', views.proceed_to_pay, name='proceedtopay'),


    path('orders/', views.orders, name='orders'),
    path('orders-details/<int:id>/', views.ordersdetails, name='ordersdetails'),
    path('orderstatus/', views.orderstatus, name='orderstatus'),



]
