from django.contrib import admin
from bookings.models import Booking
from accounts.models import UserProfile
from classes.models import Category, StudioClass

class BookingAdmin(admin.ModelAdmin):
    list_display = ['user', 'studio_class', 'status', 'stripe_payment_id']

admin.site.register(Booking, BookingAdmin)