from django.urls import path

from manageldapusers import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('forgotpassword', views.forgot_password, name='forgotpassword'),
]