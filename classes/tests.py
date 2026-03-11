from django.test import TestCase
from .models import Category

class CategoryTestCase(TestCase):

    def setUp(self):
        self.category = Category.objects.create(
            name="Pottery",
            slug="pottery",
            
        )

    def test_category_str_returns_name(self):
        self.assertEqual(str(self.category), "Pottery")

    def test_category_saves_correctly(self):
        self.assertEqual(self.category.name, "Pottery")   
        self.assertEqual(self.category.slug, "pottery")
       
        


