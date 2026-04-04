from django.shortcuts import render, redirect
from classes.models import StudioClass
from django.contrib.auth.decorators import login_required
import stripe
from django.conf import settings



stripe.api_key = settings.STRIPE_SECRET_KEY


@login_required
def stripe_checkout(request, slug):
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
        success_url=request.build_absolute_uri('/book/success') + '?success=true',
        cancel_url=request.build_absolute_uri(f'/classes/{slug}/'),
    )
    return redirect(session.url, code=303) 
def success(request):
    return render(request, 'bookings/success.html')
