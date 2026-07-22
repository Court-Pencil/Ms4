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
from datetime import date
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string




stripe.api_key = settings.STRIPE_SECRET_KEY


@login_required
def stripe_checkout(request, slug):
    class_details = StudioClass.objects.get(slug=slug)

    already_booked = Booking.objects.filter(
        user=request.user,
        studio_class=studio_class,
        status='confirmed'
        ).exists()
    if already_booked:
        messages.warning(request, 'You have already booked this class.')
        return redirect('class_details', slug=slug)
    if studio_class.is_full:
        messages.warning(request, 'Sorry, this class is fully booked.')
        return redirect('class_details', slug=slug)

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
    
        booking = Booking.objects.create(
            user = user,
            studio_class = studio_class,
            status = 'confirmed',
            stripe_payment_id = session.payment_intent
        )

        subject = f'Booking Confirmed — {studio_class.title}'
        message = render_to_string('bookings/confirmation_email.txt', {
        'user': user,
        'studio_class': studio_class,
        'booking': booking,
        })
        send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
        )
    
    return HttpResponse(status=200)
   

def success(request):
    booking_sucess = Booking.objects.filter(user=request.user, status='confirmed').order_by('-booked_at').first()
    return render(request, 'bookings/success.html', {'booking': booking_sucess})

@login_required
def my_bookings(request):
    past_bookings = Booking.objects.filter(user=request.user, status='confirmed', studio_class__date__lt=date.today())
    upcoming_bookings = Booking.objects.filter(user=request.user, status='confirmed', studio_class__date__gte=date.today())
    return render(request, 'bookings/my_bookings.html', {'past_bookings': past_bookings, 'upcoming_bookings': upcoming_bookings})

@login_required
def cancel_booking(request, booking_id):
    booking = Booking.objects.get(id=booking_id)
    if not request.user == booking.user:
        return redirect('my_bookings')
    if request.method == 'GET':
        return render(request, 'bookings/confirm_cancel_booking.html', {'booking': booking})
    if request.method == 'POST':
        booking.delete()  
        messages.success(request, 'Your booking has been cancelled.')  
    return redirect('my_bookings')
    
@login_required
def edit_booking_additional_notes(request, booking_id):
    booking = Booking.objects.get(id=booking_id)
    if not request.user == booking.user:
        return redirect('my_bookings')
    if request.method == 'POST':
        additional_notes = request.POST.get('additional_notes')
        booking.additional_notes = additional_notes
        booking.save()
        messages.success(request, 'Your additional notes have been updated.')
        return redirect('my_bookings')
    return render(request, 'bookings/edit_additional_notes.html', {'booking': booking})
    

