from django.urls import path
from .views import (
    class_list,
    class_details,
    create_class_view,
    edit_class_view,
    delete_class_view,
    submit_review,
)

urlpatterns = [
    path('', class_list, name = 'class_list'),
    path('create/', create_class_view, name='create_class_view'),
    path('<slug:slug>/edit/', edit_class_view, name='edit_class_view'),
    path('<slug:slug>/delete/', delete_class_view, name='delete_class_view'),
    path('<slug:slug>/', class_details, name='class_details'),
    path('<slug:slug>/review/', submit_review, name='submit_review'),
    
]

