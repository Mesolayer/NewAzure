from django.test import TestCase, Client
from django.urls import reverse
from engine.models import *
from django.contrib.auth.models import User

# Create your tests here.
class LogInTest(TestCase):
    def setUp(self):
        self.credentialsSuccess = {
            'username':'testuser',
            'email':'testuser@gmail.com',
            'password': 'secret'
        }

        self.credentialsFailure = {
            'username':'notexistuser',
            'email':'notexistuser@gmail.com',
            'password': 'secret'
        }
        User.objects.create_user(**self.credentialsSuccess)

    def test_login_page_url(self):
        response = self.client.get("/login/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='html/users/login.html')

    def test_login_page_view_name(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='html/users/login.html')

    def test_login_form_valid(self):
        response = self.client.post(reverse('login'), self.credentialsSuccess)
        self.assertEqual(response.status_code, 302)

    def test_login_form_invalid(self):
        response = self.client.post(reverse('login'), self.credentialsFailure)
        self.assertEqual(response.status_code, 200)

    def test_login_invalid_username_password(self):
        response = self.client.login(username="invalid",password="invalid")
        self.assertFalse(response)
    def test_login_invalid_username(self):
        response = self.client.login(username="invalid",password="secret")
        self.assertFalse(response)
    def test_login_invalid_password(self):
        response = self.client.login(username="testuser",password="invalid")
        self.assertFalse(response)
    def test_login_valid(self):
        response = self.client.login(username="testuser",password="secret")
        self.assertTrue(response)
