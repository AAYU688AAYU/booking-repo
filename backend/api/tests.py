from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from .models import Destination, TourPackage, Booking

User = get_user_model()


class AuthAndRBACApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.traveller = User.objects.create_user(
            email='traveller@voyagecraft.com',
            password='TestPassword123!',
            full_name='Test Traveller',
            role='TRAVELLER'
        )
        self.admin_user = User.objects.create_superuser(
            email='admin@voyagecraft.com',
            password='AdminPassword123!',
            full_name='Platform Admin'
        )

    def test_user_registration(self):
        response = self.client.post('/api/auth/register/', {
            'email': 'newtraveller@voyagecraft.com',
            'password': 'SecurePassword88!',
            'password_confirm': 'SecurePassword88!',
            'full_name': 'New Explorer',
            'role': 'TRAVELLER',
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertEqual(response.data['user']['email'], 'newtraveller@voyagecraft.com')

    def test_jwt_login(self):
        response = self.client.post('/api/auth/login/', {
            'email': 'traveller@voyagecraft.com',
            'password': 'TestPassword123!',
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertEqual(response.data['user']['role'], 'TRAVELLER')

    def test_user_profile_authenticated(self):
        # Authenticate with JWT
        self.client.force_authenticate(user=self.traveller)
        response = self.client.get('/api/auth/profile/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'traveller@voyagecraft.com')
        self.assertEqual(response.data['full_name'], 'Test Traveller')

    def test_rbac_admin_analytics_forbidden_for_traveller(self):
        # Traveller attempting to view admin analytics
        self.client.force_authenticate(user=self.traveller)
        response = self.client.get('/api/admin/analytics/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_rbac_admin_analytics_allowed_for_admin(self):
        # Admin accessing analytics
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get('/api/admin/analytics/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total_revenue', response.data)
