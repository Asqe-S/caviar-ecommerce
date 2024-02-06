from django.urls import path
from brands import views
urlpatterns = [
    path('', views.brands, name='brands'),
    path('get-brands/<int:id>/', views.getbrands, name='getbrands'),
    path('block-brands/<int:id>/', views.blockbrands, name='blockbrands'),
]
