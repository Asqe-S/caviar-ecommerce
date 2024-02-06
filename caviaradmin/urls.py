from django.urls import path
from caviaradmin import views
urlpatterns = [
    path('', views.admin_login, name='adminlogin'),
    path('admin-signout/', views.adminsignout, name='adminsignout'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('admin-details/', views.admindetails, name='admindetails'),


]
