from django.urls import path
from .views import book

urlpatterns = [
    path('<slug:slug>/book/', book, name='booking_page'),
]