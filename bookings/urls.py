from django.urls import path
from .views import stripe_checkout, success, stripe_webhook, my_bookings

urlpatterns = [
    path('<slug:slug>/book/', stripe_checkout, name='stripe_checkout'),
    path('book/success/', success, name='success_page'),
    path('webhook/', stripe_webhook, name='stripe_webhook'),
    path('mybookings/', my_bookings, name='my_bookings'),
]