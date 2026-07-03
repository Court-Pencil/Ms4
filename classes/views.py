from django.shortcuts import render, redirect
from classes.models import StudioClass, Category, Review
from django.contrib.auth.decorators import login_required
from classes.forms import CreateClassForm, ReviewForm
from bookings.models import Booking
from django.contrib import messages

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
    if request.user.is_authenticated:
        booked_class = Booking.objects.filter(user=request.user, studio_class=class_details, status='confirmed').exists()
    else:
        booked_class = False
    form = ReviewForm()
    reviews = Review.objects.filter(studio_class=class_details).order_by('-created_at')
    return render(request, 'classes/class_detail.html', {'class_details': class_details, 'booked_class': booked_class, 'review_form': form, 'reviews': reviews})

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

@login_required
def delete_class_view(request, slug):
    if not request.user.is_staff:
        return redirect('class_list')
    studioclass = StudioClass.objects.get(slug=slug)
    if request.method == 'POST':
        studioclass.delete()
        return redirect('class_list')
    return render(request, 'classes/class_confirm_delete.html', {'object': studioclass})

@login_required
def submit_review(request, slug):
    studioclass = StudioClass.objects.get(slug=slug)
    booked = Booking.objects.filter(
        user=request.user,
        studio_class=studioclass,
        status='confirmed'
    ).exists()
    if not booked:
        return redirect('class_details', slug=slug)

    existing_review = Review.objects.filter(
        user=request.user,
        studio_class=studioclass
    ).exists()
    if existing_review:
        messages.info(request, 'You have already reviewed this class.')
        return redirect('my_bookings')

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.studio_class = studioclass
            review.save()
            messages.success(request, 'Review submitted successfully!')
            return redirect('my_bookings')
    else:
        form = ReviewForm()
    return render(request, 'classes/submit_review.html', {'class_details': studioclass, 'review_form': form})