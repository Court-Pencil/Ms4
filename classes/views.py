from django.shortcuts import render
from classes.models import StudioClass, Category

def class_list(request):
    class_list = StudioClass.objects.all()
    filter_categories = Category.objects.all()
    class_type = request.GET.get('class_type')
    if class_type:
        class_list = class_list.filter(category__slug=class_type)
    search = request.GET.get('search')
    if search:
        filtered_class_list = class_list.filter(title__icontains=search)
    else:
        filtered_class_list = class_list
    return render(request, 'classes/class_list.html', {'class_list': filtered_class_list, 'filter_categories': filter_categories})


def class_details(request, slug):
    class_details = StudioClass.objects.get(slug=slug)
    return render(request, 'classes/class_detail.html', {'class_details': class_details})
