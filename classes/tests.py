from django.test import TestCase
from .models import Category, StudioClass
from django.contrib.auth.models import User
from bookings.models import Booking
from datetime import date
from django.db import IntegrityError
import unittest

import datetime

class CategoryModelTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(
            name="Pottery",
            slug="pottery",
            description="A class for pottery enthusiasts."
        )

    def test_category_str_returns_name(self):
        self.assertEqual(str(self.category), "Pottery")

    def test_category_saves_correctly(self):
        self.assertEqual(self.category.name, "Pottery")   
        self.assertEqual(self.category.slug, "pottery")
        self.assertEqual(self.category.description, "A class for pottery enthusiasts.")

class StudioClassModelTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(
            name="Pottery",
            slug="pottery",
            description="A class for pottery enthusiasts."
        )
        self.studioclass = StudioClass.objects.create(
            title = 'Intro to Pottery',
            category = self.category,
            instructor = 'Steve',
            date = date(2024, 7, 1),
            duration = 120,
            capacity = 10,
            price = 50.00,
            description = 'Learn the basics of pottery in this introductory class.',
            is_published = True,
        )

    
    def test_studioclass_spots_remaining(self):
        self.assertEqual(self.studioclass.spots_remaining, 10)

   
    def test_spots_remaining_decreases_with_booking(self):
        self.user = User.objects.create_user(username='court', password='testuser123')
        Booking.objects.create(
        user=self.user,
        studio_class=self.studioclass,
        status='confirmed',
        stripe_payment_id='fushgui1033'
    )
        self.assertEqual(self.studioclass.spots_remaining, 9)

    
    def test_is_full_returns_false_when_spots_available(self):
        self.assertFalse(self.studioclass.is_full)

    def test_studioclass_str_returns_name(self):
        self.assertEqual(str(self.studioclass), "Intro to Pottery")

    
class BookingModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name="Pottery",
            slug="pottery",
            description="A class for pottery enthusiasts."
        )
        self.studioclass = StudioClass.objects.create(
            title = 'Intro to Pottery',
            category = self.category,
            instructor = 'Steve',
            date = date(2024, 7, 1),
            duration = 120,
            capacity = 10,
            price = 50.00,
            description = 'Learn the basics of pottery in this introductory class.',
            is_published = True,
        )
        self.user = User.objects.create_user(username='court', password='testuser123')
        self.booking = Booking.objects.create(
            user = self.user,
            studio_class = self.studioclass,
            status = 'confirmed',
            stripe_payment_id = 'fushgui1033'
        )

    def test_booking_saves_correctly(self):
        self.assertEqual(self.booking.user , self.user)
        self.assertEqual(self.booking.studio_class , self.studioclass)
        self.assertEqual(self.booking.status , 'confirmed') 
        self.assertEqual(self.booking.stripe_payment_id , 'fushgui1033')

    def test_booking_status_default_pending(self):
        new_user = User.objects.create_user(
        username='newuser', 
        password='testpass123'
        )
        booking = Booking.objects.create(
            user=new_user,
            studio_class=self.studioclass,
            stripe_payment_id='abc456'
            )
        self.assertEqual(booking.status, 'pending')

    def test_no_double_booking(self):
        with self.assertRaises(IntegrityError):
            Booking.objects.create(
                user=self.user,
                studio_class=self.studioclass,
                status='confirmed',
                stripe_payment_id='abc123'
        )
    def test_all_bookings_for_specific_user(self):
        user_bookings = Booking.objects.filter(user=self.user)
        self.assertEqual(user_bookings.count(), 1)

    def test_all_bookings_for_specific_studio_class(self): 
        studio_class_bookings = Booking.objects.filter(studio_class=self.studioclass) 
        self.assertEqual(studio_class_bookings.count(), 1)
        

              


