from django.contrib import admin
from accounts.models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone_number']

admin.site.register(UserProfile, UserProfileAdmin)