from django.test import TestCase
from .models import Category, StudioClass

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
            category = 'Pottery',
            instructor = 'Steve',
            date = '03/03/26',
            duration = '2 hours',
            capacity = 10,
            price = 50.00,
            image = 'path/to/image.jpg',
            descritpion = 'Learn the basics of pottery in this introductory class.',
            is_published = True,
        )
        


