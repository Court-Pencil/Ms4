from django.test import TestCase
from .models import Category, StudioClass, Review
from django.contrib.auth.models import User
from bookings.models import Booking
from accounts.models import UserProfile
from datetime import date
from django.db import IntegrityError
from django.core.exceptions import ValidationError
import decimal
from decimal import Decimal


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

    def test_studioclass_returns_slug(self):
        self.assertEqual(str(self.studioclass.slug), "intro-to-pottery")
    
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
        
    

class ReviewModelTest(TestCase):
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
        self.review = Review.objects.create(
            user = self.user,
            studio_class = self.studioclass,
            rating = 5,
            comment = "Great class! Learned a lot and had fun.",
        )

    def test_review_saves_correctly(self):
        self.assertEqual(self.review.user , self.user)
        self.assertEqual(self.review.studio_class , self.studioclass)
        self.assertEqual(self.review.rating , 5) 
        self.assertEqual(self.review.comment , "Great class! Learned a lot and had fun.")

    def test_rating_validator_one_to_five(self):
        new_user = User.objects.create_user(
        username='newuser', 
        password='testpass123'
        )
        with self.assertRaises(ValidationError):
            review = Review.objects.create(
            user = new_user,
            studio_class = self.studioclass,
            rating = 0,
            comment = "fail test",
            )
            review.full_clean()

    def test_rating_validator_rejects_over_five(self):
        new_user2 = User.objects.create_user(
        username='newuser', 
        password='testpass123'
        )
        with self.assertRaises(ValidationError):
            review = Review.objects.create(
            user = new_user2,
            studio_class = self.studioclass,
            rating = 6,
            comment = "fail test",
            )
            review.full_clean()

    def test_one_review_per_person(self):
        with self.assertRaises(IntegrityError):
            Review.objects.create(
            user = self.user,
            studio_class = self.studioclass,
            rating = 5,
            comment = "Great class! Learned a lot and had fun.",
        )
            
class UserProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='jessica', password='testuser123'
        )
        self.userprofile = self.user.accounts
        
    def test_user_profile_returns_correct_user(self):
        self.assertEqual(self.userprofile.user, self.user)
    def test_user_profile_str_returns_name(self):
        self.assertEqual(str(self.userprofile), "jessica")

    def test_user_profile_saves_correctly(self):
        self.assertEqual(self.userprofile.bio, '')
        self.assertEqual(self.userprofile.phone_number, '')

    def test_on_user_creation_create_profile(self):
        new_user = User.objects.create_user(username='newuser', password='123rr')
        self.assertTrue(UserProfile.objects.filter(user=new_user).exists())

class ClassViewTest(TestCase):
    def test_public_class_view(self):
        response = self.client.get("/classes/")
        self.assertEqual(200, response.status_code)

class ClassCRUDViewTest(TestCase):

    def test_only_admin_can_acess_the_create_class_view(self):
        new_user = User.objects.create_user(
        username='newuser', 
        password='testpass123'
        )
        self.client.login(username='newuser', password='testpass123')
        response = self.client.get("/classes/create/")
        self.assertEqual(302, response.status_code)

    def test_class_form_saves_correctly(self):
        admin = User.objects.create_user(
        username='court', 
        password='testpass123',
        is_staff=True
        )
        self.client.login(username='court', password='testpass123')
        self.client.post("/classes/create/", {
        'title': 'claymation',
        'category': Category.objects.create(name='Sculpting', slug='sculpting', description='A class for sculpting enthusiasts.').id,
        'instructor': 'Court',      
        'date': '2024-07-01',
        'duration': 120,
        'capacity': 10,
        'price': 50.00,
        'description': 'Learn the basics of claymation in this introductory class.',
        'is_published': True
        })
        new_class = StudioClass.objects.get(title='claymation')
        self.assertEqual(new_class.title, 'claymation')
        self.assertEqual(new_class.instructor, 'Court')
        self.assertEqual(new_class.duration, 120)
        self.assertEqual(new_class.capacity, 10)
        self.assertEqual(new_class.price, 50.00)
        self.assertEqual(new_class.description, 'Learn the basics of claymation in this introductory class.')
        self.assertEqual(new_class.is_published, True)  

    def test_edit_class_form_saves_correctly(self):
        admin = User.objects.create_user(
        username='court', 
        password='testpass123',
        is_staff=True
        )
        self.client.login(username='court', password='testpass123')
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
        self.client.post("/classes/Intro to Pottery/edit/", {
        'title': 'claymation',
        'category': Category.objects.create(name='Sculpting', slug='sculpting', description='A class for sculpting enthusiasts.').id,
        'instructor': 'Court',      
        'date': '2024-07-01',
        'duration': 120,
        'capacity': 10,
        'price': 40.00,
        'description': 'Learn the basics of claymation in this introductory class.',
        'is_published': True
        })
        updated_class = StudioClass.objects.get(id=self.studioclass.id)
        self.assertEqual(updated_class.title, 'Updated Pottery')
        self.assertEqual(updated_class.price, Decimal('40.00'))

    def test_non_admin_cannot_access_edit_class_view(self):
        new_user = User.objects.create_user(
        username='newuser', 
        password='testpass123'
        )
        self.client.login(username='newuser', password='testpass123')
        response = self.client.get("/classes/intro-to-pottery/edit/")
        self.assertEqual(302, response.status_code)

       
    




    
    


