from django.urls import path
from product import views
urlpatterns = [
    path('product/<int:id>/', views.product, name='product'),

    path('block-product/', views.blockproduct, name='blockproduct'),
    path('add-product/', views.addproduct, name='addproduct'),
    path('edit-product/<int:id>/', views.editproducts, name='editproducts'),

    path('add-varient/', views.addvarient, name='addvarient'),
    path('edit-varient/<int:id>/', views.editvarient, name='editvarient'),


    path('get-category/', views.getcategory, name='getcategory'),
    path('get-subcategory/', views.getsubcategory, name='getsubcategory'),

    path('review', views.review, name='review')

]
