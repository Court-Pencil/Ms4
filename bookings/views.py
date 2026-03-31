from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from classes.models import StudioClass


@login_required
def book(request, slug):
    class_details = StudioClass.objects.get(slug=slug)
    bookings = class_details.bookings.filter(user=request.user)
    return render(request, 'bookings/bookings_page.html', {'class_details': class_details, 'bookings': bookings})
   
