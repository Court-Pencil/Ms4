from django.shortcuts import render, redirect
from classes.models import StudioClass
from django.contrib.auth.decorators import login_required
from classes.models import StudioClass
import stripe
from django.conf import settings



stripe.api_key = settings.STRIPE_SECRET_KEY


@login_required
def book(request, slug):
    class_details = StudioClass.objects.get(slug=slug)
    bookings = class_details.bookings.filter(user=request.user)
    return render(request, 'bookings/bookings_page.html', {'class_details': class_details, 'bookings': bookings})
   
@login_required
def create_checkout_session(request, slug):
    class_details = StudioClass.objects.get(slug=slug)
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'gbp',
                'product_data': {
                    'name': class_details.title,
                },
                'unit_amount': int(class_details.price * 100),
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=request.build_absolute_uri('/classes/sucess') + '?success=true',
        cancel_url=request.build_absolute_uri('/classes/<slug:slug>/') + '?canceled=true',
    )
    return redirect(session.url, code=303)

def success(request):
    return render(request, 'bookings/success.html')
