from django.test import TestCase
from accounts.models import UserProfile
from django.contrib.auth.models import User

class AuthViewTest(TestCase):

    def test_anon_can_acess_login_page(self):
        response = self.client.get("/accounts/login/")
        self.assertEqual(200, response.status_code)

    def test_anon_can_acess_signup_page(self):
        response = self.client.get("/accounts/signup/")
        self.assertEqual(200, response.status_code)

    def test_auth_user_gets_redirected(self):
        new_user = User.objects.create_user(
        username='newuser', 
        password='testpass123'
        )
        self.client.login(username='newuser', password='testpass123')
        response = self.client.get("/accounts/login/")
        self.assertEqual(302, response.status_code)
    
    def test_cannot_anon_access_userprofile(self):
        response = self.client.get("/accounts/")
        self.assertEqual(302, response.status_code)

    def test_logged_in_user_can_access_userprofile(self):
        new_user = User.objects.create_user(
        username='newuser', 
        password='testpass123'
        )
        self.client.login(username='newuser', password='testpass123')
        response = self.client.get("/userprofile/")
        self.assertEqual(200, response.status_code)

    def test_user_can_login(self):
        User.objects.create_user(
        username='newuser',
        password='testpass123'
        )
        logged_in = self.client.login(username='newuser', password='testpass123')
        self.assertTrue(logged_in)

    def test_does_form_display_to_logged_in_user(self):
        new_user = User.objects.create_user(
        username='newuser', 
        password='testpass123'
        )
        self.client.login(username='newuser', password='testpass123')
        response = self.client.get("/userprofile/edit/")
        self.assertEqual(200, response.status_code)

    def test_form_saves_correctly(self):
        new_user = User.objects.create_user(username='newuser', password='testpass123')
        self.client.login(username='newuser', password='testpass123')
        self.client.post("/userprofile/edit/", {
        'phone_number': '0123456789',
        'bio': 'Updated bio'
        })
        updated_profile = UserProfile.objects.get(user=new_user)
        self.assertEqual(updated_profile.phone_number, '0123456789')
        self.assertEqual(updated_profile.bio, 'Updated bio')




