from django.test import TestCase
from .models import Booking
from classes.models import StudioClass, Category
from django.contrib.auth.models import User
from datetime import date

class CancellationTestCase(TestCase):
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

    def test_cancel_booking_deletes_booking(self):
        self.client.login(username='court', password='testuser123')
        response = self.client.post(f"/bookings/book/{self.booking.id}/cancel/")
        self.assertEqual(302, response.status_code)
        self.assertFalse(Booking.objects.filter(id=self.booking.id).exists())

