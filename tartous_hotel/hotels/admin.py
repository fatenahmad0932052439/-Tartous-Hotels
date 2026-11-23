from django.contrib import admin

from django.contrib import admin
from .models import Hotel, Room, Booking


class RoomInline(admin.TabularInline):
    model = Room
    extra = 1


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'stars', 'address')
    list_filter = ('city', 'stars')
    search_fields = ('name', 'address')
    inlines = [RoomInline]


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('hotel', 'room_number', 'room_type', 'capacity', 'price_per_night', 'has_sea_view')
    list_filter = ('hotel', 'room_type', 'has_sea_view')


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('booking_code', 'guest_name', 'room', 'check_in', 'check_out', 'total_price', 'status')
    list_filter = ('status', 'check_in')
    search_fields = ('booking_code', 'guest_name', 'guest_email')
