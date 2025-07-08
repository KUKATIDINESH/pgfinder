from django.urls import path
from . import views
urlpatterns=[
    path('home',views.home,name='home'),
    path('display_all_pg_details/<str:area>/<str:rent>/',views.display_all_pg_details,name='display_all_pg_details'),
    path('aboutus',views.about_us,name='aboutus'),
    path('pgregister',views.PGregister,name='pgregister'),
    path('pgdetails/<int:pk>',views.pg_details,name='pgdetails'),
    path('modifypg/<int:pk>',views.pg)
    
]