from django.test import TestCase

class AuthViewTest(TestCase):

    def test_anon_can_acess_login_page(self):
        response = self.client.get("/accounts/login/")
        self.assertEqual(200, response.status_code)

    def test_anon_can_acess_login_page(self):
        response = self.client.get("/accounts/signup/")
        self.assertEqual(200, response.status_code)
