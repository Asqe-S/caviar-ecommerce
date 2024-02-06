from django.urls import path
from security import views
urlpatterns = [
    path('', views.signin, name='signin'),
    path('signout', views.signout, name='signout'),
    path('signup/', views.signup, name='signup'),
    path('otp/', views.otp, name='otp'),
    path('password recovey/', views.forgotpassword, name='forgotpassword'),
    path('recovery-email/', views.femail, name='femail')

]
