from django.shortcuts import render, redirect
from classes.models import StudioClass
from django.contrib.auth.decorators import login_required
import stripe
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json
from .models import Booking
from django.contrib.auth.models import User



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
        metadata={
            'class_slug': slug,
            'user_id': request.user.id,
            },
        mode='payment',
        success_url=request.build_absolute_uri('/bookings/book/success/') + '?success=true',
        cancel_url=request.build_absolute_uri(f'/classes/{slug}/'),
    )
    return redirect(session.url, code=303) 

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)
    
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        class_data = session.metadata.class_slug
        user_id = session.metadata.user_id

        studio_class = StudioClass.objects.get(slug=class_data) 
        user = User.objects.get(id=user_id)
    
        Booking.objects.create(
            user = user,
            studio_class = studio_class,
            status = 'confirmed',
            stripe_payment_id = session.payment_intent
        )
    
    return HttpResponse(status=200)
   

def success(request):
    return render(request, 'bookings/success.html')
