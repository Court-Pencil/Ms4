from django.urls import path
from .views import stripe_checkout, success

urlpatterns = [
    path('<slug:slug>/book/', stripe_checkout, name='stripe_checkout'),
    path('book/success/', success, name='success_page'),
]