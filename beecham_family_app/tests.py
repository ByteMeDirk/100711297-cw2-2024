from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class UserAuthenticationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')

    def test_user_login(self):
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'testpass123'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))

    def test_user_registration(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'newpass123',
            'password2': 'newpass123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_profile_creation_on_registration(self):
        response = self.client.post(reverse('register'), {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        })
        self.assertEqual(response.status_code, 200)
        user =User.objects.get(username='testuser')
