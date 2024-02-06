from django.urls import path
from category import views
urlpatterns = [
    path('', views.category, name='category'),
    path('subcategory/', views.subcategory, name='subcategory'),

]
