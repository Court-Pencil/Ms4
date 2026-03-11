from django.test import TestCase
from .models import Catergory

class CatergoryTestCase(TestCase):

    def setUp(self):
        self.catergory = Catergory.objects.create(
            name="Pottery",
            slug="pottery",
        )

    def test_catergory_str_returns_name(self):
        self.assertEqual(str(self.catergory, "Pottery"))

    def test_catergory_saves_correctly(self):
        self.assertEqual(self.catergory.name, "Pottery")   
        self.assertEqual(self.catergory.slug, "pottery")


