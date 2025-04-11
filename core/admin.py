from django.contrib import admin
from .models import Hotel, Room, Booking

class HotelAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'state', 'town')
    search_fields = ('name', 'state', 'town')

class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_type', 'hotel', 'price_per_hour', 'is_available')
    list_filter = ('is_available', 'hotel')

class BookingAdmin(admin.ModelAdmin):
    list_display = ('guest_name', 'room', 'start_time', 'end_time', 'created_at')
    search_fields = ('guest_name', 'guest_email')

admin.site.register(Hotel, HotelAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(Booking, BookingAdmin)
