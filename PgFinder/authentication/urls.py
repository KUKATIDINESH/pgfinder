from django.urls import path
from . import views
urlpatterns=[
    path('login',views.user_login,name='login'),
    path('',views.user_login,name='login'),

    path('signin',views.signin,name='signin'),
    path('forgot_password', views.forgot_password, name='forgot_password'),
    path('verify_reset_otp', views.verify_reset_otp, name='verify_reset_otp'),
    path('reset_password', views.reset_password, name='reset_password'),
    path('logout',views.user_logout,name='logout'),
    path('verify_otp',views.verify_otp,name='verify_otp'),
#     path('',views.home,name='home')
    ]

