from django.contrib import admin
from bookings.models import Booking


class BookingAdmin(admin.ModelAdmin):
    list_display = ['user', 'studio_class', 'status', 'stripe_payment_id']

admin.site.register(Booking, BookingAdmin)