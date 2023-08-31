from datetime import timedelta
from http import HTTPStatus

from django.test.testcases import TestCase
from django.urls import reverse
from django.utils.timezone import now
from users.models import User, UserEmailVerification


class UserRegistrationTestCase(TestCase):
    fixtures = [
        'social_app.json'
    ]

    def setUp(self) -> None:
        self.path = reverse('users:registration')
        self.test_data = {
            'first_name': 'test',
            'last_name': 'test',
            'username': 'test',
            'password1': 'Sdzxasqw12',
            'password2': 'Sdzxasqw12',
            'email': 'test@gmail.com',
        }

    def test_registration_get(self):
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/registration.html')
        self.assertEqual(response.context_data['title'], 'Registration')

    def test_registration_post(self):
        username = self.test_data['username']
        user = User.objects.filter(username=username)
        self.assertFalse(user.exists())

        response = self.client.post(self.path, self.test_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('users:login'))
        self.assertTrue(user.exists())

        email_verif = UserEmailVerification.objects.filter(user__username=username)
        self.assertTrue(email_verif.exists())
        self.assertEqual(email_verif.first().expiration.date(), (now() + timedelta(minutes=60)).date())

    def test_failed_registration(self):
        self.test_registration_post()
        username = self.test_data['username']
        user = User.objects.filter(username=username)
        response = self.client.post(self.path, self.test_data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'Пользователь с таким именем уже существует.', html=True)
