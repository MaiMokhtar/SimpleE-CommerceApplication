from django.test import TestCase, Client
from django.urls import reverse

from shopping.models import Cart, Item
from profiles.models import UserProfile


class PurchaseViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = UserProfile.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')
        self.url = reverse('shopping:purchase')
        self.cart = Cart.objects.get_or_create_by_user(self.user)

    def test_purchase_view_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shopping/purchase.html')
        self.assertEqual(response.context['purchase_form'].is_bound, False)

    def test_purchase_view_post_valid(self):
        item = Item.objects.create(name='Test Item', price=10)
        data = {
            'items': [item.id],
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('shopping:cart-confirm'))
        self.assertTrue(item in self.cart.items.all())

    def test_purchase_view_post_invalid(self):
        data = {}
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shopping/purchase.html')
        self.assertEqual(response.context['purchase_form'].is_bound, True)
        self.assertFalse(response.context['purchase_form'].is_valid())


