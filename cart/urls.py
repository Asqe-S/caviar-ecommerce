from django.urls import path
from cart import views
urlpatterns = [
    path('', views.cart, name='cart'),
    path('add-to-cart', views.addtocart, name='addtocart'),
    path('add-cart-qty', views.addcartquantity, name='addcartquantity'),
    path('remove-from-cart', views.removefromcart, name='removefromcart'),
]
