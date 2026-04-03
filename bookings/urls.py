from django.urls import path
from .views import book, success, create_checkout_session

urlpatterns = [
    path('<slug:slug>/book/', book, name='booking_page'),
    path('book/success/', success, name='success_page'),
]