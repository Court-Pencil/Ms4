from django.shortcuts import render
from classes.models import StudioClass

def home(request):
    class_list = StudioClass.objects.all()[:3]                   
    return render(request, 'home/home.html', {'class_list': class_list})



    


