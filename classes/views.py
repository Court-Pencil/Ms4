from django.shortcuts import render
from classes.models import StudioClass

def class_list(request):
    class_list = StudioClass.objects.all()
    return render(request, 'classes/class_list.html', {'class_list': class_list})
