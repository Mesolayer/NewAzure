from django.test import TestCase
from django.urls import reverse
from engine.models import *
from django.contrib.auth.models import User
# Create your tests here.
class AchievementsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='dummy',
                                        email='dummy@dummy.com',
                                        password='dummy_for_test_123')
        

    def test_achievements_needs_login(self):
        response = self.client.get(reverse('achievements'))

        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, '/login/?next=/achievements/')


    def test_achievements_show(self):
        self.client.login(username='dummy', password='dummy_for_test_123')
        response = self.client.get(reverse('achievements'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='html/achievements/achievements.html')
