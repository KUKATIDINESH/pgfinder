from django.urls import path
from . import views
urlpatterns=[
    path('login',views.user_login,name='login'),
    path('',views.user_login,name='login'),

    path('signin',views.signin,name='signin'),
    path('logout',views.user_logout,name='logout'),
    path('verify_otp',views.verify_otp,name='verify_otp'),
#     path('',views.home,name='home')
    ]

