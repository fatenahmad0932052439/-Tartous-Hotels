from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('booking/', views.booking_page, name='booking_page'),
    path('hotel/<int:hotel_id>/', views.hotel_detail, name='hotel_detail'),
    path('booking/room/<int:room_id>/', views.book_room, name='book_room'),
    path('booking/success/<str:booking_code>/', views.booking_success, name='booking_success'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('booking/cancel/<str:booking_code>/', views.cancel_booking, name='cancel_booking'),
]