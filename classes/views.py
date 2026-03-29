from django.shortcuts import render, redirect
from classes.models import StudioClass, Category
from django.contrib.auth.decorators import login_required
from classes.forms import CreateClassForm

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

@login_required
def create_class_view(request):
    if not request.user.is_staff:
        return redirect('class_list')
    if request.method == 'POST':
        form = CreateClassForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('class_list')
    else:
        form = CreateClassForm()
    return render(request, 'classes/create_class_view.html/', {'form': form})

@login_required
def edit_class_view(request, slug):
    if not request.user.is_staff:
        return redirect('class_list')
    studioclass = StudioClass.objects.get(slug=slug)
    if request.method == 'POST':
        form = CreateClassForm(request.POST, request.FILES, instance=studioclass)
        if form.is_valid():
            form.save()
            return redirect('class_details', slug=studioclass.slug)
    else:
        form = CreateClassForm(instance=studioclass)
    return render(request, 'classes/edit_class_view.html', {'form': form, 'studioclass': studioclass})
