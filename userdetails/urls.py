from django.urls import path
from userdetails import views
urlpatterns = [
    path('', views.userdata, name='userdetails'),
    path('edit/<int:id>/', views.edituser, name='edituser'),
    path('change-password/<int:id>/', views.changepassword, name='changepassword'),
    path('add-address/', views.addaddress, name='addaddress'),
    path('edit-address/<int:id>/', views.editaddress, name='editaddress'),
    path('get-address/<int:id>/', views.getaddress, name='getaddress'),
    path('delete-address/<int:id>/', views.deleteaddress, name='deleteaddress'),



    path('users/', views.users, name='users'),
    path('blockusers/<int:id>/', views.blockusers, name='blockusers'),

]
