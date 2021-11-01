from django.urls import path

from manageldapusers import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('forgotpassword', views.forgot_password, name='forgotpassword'),
    path('resetpassword/<str:token>', views.reset_password, name='resetpassword'),
    path('activation/<str:activation_token>', views.activate_account, name='activateaccount'),
]
