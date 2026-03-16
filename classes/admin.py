from django.contrib import admin
from classes.models import Category, StudioClass

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']

admin.site.register(Category, CategoryAdmin)

class StudioClassAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'instructor', 'date', 'duration', 'capacity', 'price', 'is_published']
    
admin.site.register(StudioClass, StudioClassAdmin)



