from django.test import TestCase
from .models import Category, StudioClass
from django.contrib.auth.models import User
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
            date = '03/03/26',
            duration = '2 hours',
            capacity = 10,
            price = 50.00,
            image = 'path/to/image.jpg',
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

    

    
              


