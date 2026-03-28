from django.urls import path
from .views import class_list, class_details, create_class_view

urlpatterns = [
    path('', class_list, name = 'class_list'),
    path('create/', create_class_view, name='create_class_view'),
    path('<slug:slug>/', class_details, name='class_details')
    
]