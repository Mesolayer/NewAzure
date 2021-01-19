from django.test import TestCase, Client
from django.urls import reverse
from engine.models import UserData
from django.contrib.auth.models import User

# Create your tests here.
class SignUpTest(TestCase):
    def setUp(self) -> None:
        self.username = 'testuser'
        self.email = 'testuser@email.com'
        self.password = 'valid123Password'

    def test_signup_page_url(self):
        response = self.client.get("/register/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='html/users/register.html')

    def test_signup_page_view_name(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='html/users/register.html')


    def test_signup_form_invalid_password(self):
        response = self.client.post(reverse('register'), data={
            'username': self.username,
            'email': self.email,
            'password1': 'invalid',
            'password2': 'invalid'
        })
        self.assertEqual(response.status_code, 200)

        users = User.objects.all()
        userData = UserData.objects.all()
        self.assertEqual(users.count(), 0)
        self.assertEqual(userData.count(), 0)

    def test_signup_form_invalid_email(self):
        response = self.client.post(reverse('register'), data={
            'username': self.username,
            'email': 'notanemail',
            'password1': self.password,
            'password2': self.password
        })
        self.assertEqual(response.status_code, 200)

        users = User.objects.all()
        userData = UserData.objects.all()
        self.assertEqual(users.count(), 0)
        self.assertEqual(userData.count(), 0)


    def test_signup_form_valid(self):
        response = self.client.post(reverse('register'), data={
            'username': self.username,
            'email': self.email,
            'password1': self.password,
            'password2': self.password
        })
        self.assertEqual(response.status_code, 302)


        users = User.objects.all()
        userData = UserData.objects.all()
        self.assertEqual(users.count(), 1)
        self.assertEqual(userData.count(), 1)

    def test_signup_form_existing_user(self):
        response = self.client.post(reverse('register'), data={
            'username': self.username,
            'email': self.email,
            'password1': self.password,
            'password2': self.password
        })
        self.assertEqual(response.status_code, 302)

        response2 = self.client.post(reverse('register'), data={
            'username': self.username,
            'email': self.email,
            'password1': self.password,
            'password2': self.password
        })
        self.assertEqual(response2.status_code, 200)

        users = User.objects.all()
        userData = UserData.objects.all()
        self.assertEqual(users.count(), 1)
        self.assertEqual(userData.count(), 1)
