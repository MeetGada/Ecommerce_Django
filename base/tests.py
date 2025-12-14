from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from base.models import User, Product

class UserTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('register')
        self.login_url = reverse('token_obtain_pair')
        self.user_data = {
            'name': 'Test User',
            'email': 'test@test.com',
            'password': 'testpassword123'
        }

    def test_registration(self):
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('token' in response.data)
        self.assertEqual(User.objects.count(), 1)

    def test_login(self):
        # Register first
        self.client.post(self.register_url, self.user_data)
        
        login_data = {
            'email': 'test@test.com',
            'password': 'testpassword123'
        }
        response = self.client.post(self.login_url, login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in response.data)

class ProductTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = User.objects.create_superuser('admin@test.com', 'admin@test.com', 'password123')
        self.user = User.objects.create_user('user@test.com', 'user@test.com', 'password123')
        
    def test_get_products_public(self):
        url = reverse('products')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_product_admin(self):
        self.client.force_authenticate(user=self.admin)
        url = reverse('product-create')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Product.objects.count(), 1)

    def test_create_product_non_admin(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('product-create')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
