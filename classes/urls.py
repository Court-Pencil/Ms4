from django.urls import path
from .views import class_list, class_details

urlpatterns = [
    path('', class_list, name = 'class_list'),
    path('<slug:slug>/', class_details, name='class_details')
]