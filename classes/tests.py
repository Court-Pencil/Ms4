from django.test import TestCase
from .models import Category, StudioClass
from django.contrib.auth.models import User
from bookings.models import Booking
from datetime import date
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
            date = datetime(2024, 7, 1),
            duration = 120,
            capacity = 10,
            price = 50.00,
            description = 'Learn the basics of pottery in this introductory class.',
            is_published = True,
        )

    @unittest.skip("Booking model not built yet")
    def test_studioclass_spots_remaining(self):
        self.assertEqual(self.studioclass.spots_remaining, 10)

    @unittest.skip("Booking model not built yet")
    #def test_spots_remaining_decreases_with_booking(self):

    @unittest.skip("Booking model not built yet")
    #def test_is_full_returns_false_when_spots_available(self):

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
        

              


