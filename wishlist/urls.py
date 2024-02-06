from django.urls import path
from wishlist import views
urlpatterns = [
    path('', views.wishlist, name='wishlist'),
    path('add-to-wishlist/', views.addtowishlist, name='addtowishlist'),
    path('remove-from-wishlist/', views.rmwishlist, name='rmfromwishlist'),
]
