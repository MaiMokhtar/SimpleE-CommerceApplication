from django.test import TestCase, Client
from django.urls import reverse_lazy
from django.urls import reverse

from profiles.models import UserProfile
from profiles.views import LoginView


class LoginViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse_lazy('profiles:login')
        self.user = UserProfile.objects.create_user(username='testuser', password='testpass')

    def test_unauthenticated_user(self):
        # Test GET request when user is not authenticated
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/login.html')

    def test_authenticated_user(self):
        # Test GET request when user is authenticated
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('shopping:purchase'))

    def test_get_success_url(self):
        view = LoginView()
        self.assertEqual(view.get_success_url(), reverse_lazy('shopping:purchase'))


class LogoutViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse_lazy('profiles:logout')
        self.user = UserProfile.objects.create_user(username='testuser', password='testpass')

    def test_authenticated_user_redirected(self):
        # Test GET request when user is authenticated
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('profiles:login'))

    def test_unauthenticated_user_gets_login_page(self):
        response = self.client.get(reverse('profiles:login'))
        self.assertTemplateUsed(response, 'profiles/login.html')
        self.assertEqual(response.status_code, 200)

