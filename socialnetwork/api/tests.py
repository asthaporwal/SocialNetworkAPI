from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from api.models import FriendRequest

User = get_user_model()

class SignupTest(APITestCase):
    def test_signup(self):
        url = reverse('signup')
        data = {
            'email': 'testuser@example.com',
            'password': 'testpassword123',
            'name': 'Test User'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, 'testuser@example.com')

class LoginTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='testuser@example.com', password='testpassword123')
        self.url = reverse('login')

    def test_login(self):
        data = {
            'email': 'testuser@example.com',
            'password': 'testpassword123'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

class SearchUsersTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='testuser@example.com', password='testpassword123', name='Test User')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_search_users(self):
        url = reverse('search') + '?q=Test'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['email'], 'testuser@example.com')

class SendFriendRequestTest(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(email='user1@example.com', password='password123', name='User One')
        self.user2 = User.objects.create_user(email='user2@example.com', password='password123', name='User Two')
        self.token = Token.objects.create(user=self.user1)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_send_friend_request(self):
        url = reverse('friend-request')
        data = {
            'to_user': self.user2.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['from_user'], self.user1.id)
        self.assertEqual(response.data['to_user'], self.user2.id)

class AcceptRejectFriendRequestTest(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(email='user1@example.com', password='password123', name='User One')
        self.user2 = User.objects.create_user(email='user2@example.com', password='password123', name='User Two')
        self.token = Token.objects.create(user=self.user2)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.friend_request = FriendRequest.objects.create(from_user=self.user1, to_user=self.user2)

    def test_accept_friend_request(self):
        url = reverse('friend-request-action', kwargs={'id': self.friend_request.id, 'action': 'accept'})
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.friend_request.refresh_from_db()
        self.assertEqual(self.friend_request.status, 'accepted')

    def test_reject_friend_request(self):
        url = reverse('friend-request-action', kwargs={'id': self.friend_request.id, 'action': 'reject'})
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.friend_request.refresh_from_db()
        self.assertEqual(self.friend_request.status, 'rejected')

