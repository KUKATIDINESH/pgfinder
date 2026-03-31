from django.urls import path
from . import views
urlpatterns=[
    path('home',views.home,name='home'),
    path('display_all_pg_details/<str:area>/<str:rent>/',views.display_all_pg_details,name='display_all_pg_details'),
    path('aboutus',views.about_us,name='aboutus'),
    path('pgregister',views.PGregister,name='pgregister'),
    path('pgdetails/<int:pk>',views.pg_details,name='pgdetails'),
    path('modifypg/<int:pk>',views.pg_modify,name='modifypg'),
    path('pglist_for_modification',views.pglist_for_modify,name='pglist_for_modification'),
    path('pg_delete/<int:pk>', views.pg_delete,name='pg_delete'),
    path('delete_image/<int:image_id>', views.delete_image, name='delete_image'),
    
    # Booking URLs
    path('book_pg/<int:pk>', views.book_pg, name='book_pg'),
    path('my_bookings', views.my_bookings, name='my_bookings'),
    path('cancel_booking/<int:booking_id>', views.cancel_booking, name='cancel_booking'),
    path('manage_bookings', views.manage_bookings, name='manage_bookings'),
    path('update_booking_status/<int:booking_id>/<str:status>', views.update_booking_status, name='update_booking_status'),
    path('add_booking_review/<int:booking_id>', views.add_booking_review, name='add_booking_review'),
]
