from django.urls import path
from . import views
urlpatterns=[
    path('login',views.user_login,name='login'),
    path('signin',views.signin,name='signin'),
    path('logout',views.user_logout,name='logout'),
#     path('',views.home,name='home')
    ]