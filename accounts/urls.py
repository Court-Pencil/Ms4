from django.urls import path
from . import views

urlpatterns = [
    path('userprofile/', views.profile, name='profile'),
    path('userprofile/edit/', views.edit_profile, name='edit_profile'),
]