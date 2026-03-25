from django.shortcuts import render
from classes.models import StudioClass

def class_list(request):
    class_list = StudioClass.objects.all()
    return render(request, 'classes/class_list.html', {'class_list': class_list})


def class_details(request, slug):
    class_details = StudioClass.objects.get(slug=slug)
    return render(request, 'classes/class_detail.html', {'class_details': class_details})
