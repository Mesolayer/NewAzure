# Created with the help of https://www.youtube.com/watch?v=0MrgsYswT1c

from django.test import SimpleTestCase
from django.urls import reverse, resolve
from dashboard.views import *

class TestUrls(SimpleTestCase):
    
    def test_dash_url_is_resolved(self):
        url = reverse('daily-dashboard')
        self.assertEquals(resolve(url).func, daily_dashboard)


    def test_dash_filter_url_is_resolved(self):
        url = reverse('dashboard-filter')
        self.assertEquals(resolve(url).func, dashboard_filter_tags)


    def test_dash_details_url_is_resolved(self):
        url = reverse('dashboard-show-details')
        self.assertEquals(resolve(url).func, dashboard_show_details)


    def test_dash_create_task_url_is_resolved(self):
        url = reverse('create-task')
        self.assertEquals(resolve(url).func, create_task)


    def test_dash_assign_tag_url_is_resolved(self):
        url = reverse('assign-tag')
        self.assertEquals(resolve(url).func, assign_tag)


    def test_dash_create_tag_url_is_resolved(self):
        url = reverse('create-tag')
        self.assertEquals(resolve(url).func, create_tag)


    def test_dash_complete_task_url_is_resolved(self):
        url = reverse('complete-task')
        self.assertEquals(resolve(url).func, complete_task)


    def test_update_task_url_is_resolved(self):
        url = reverse('update-task')
        self.assertEquals(resolve(url).func, update_task)


    def test_delete_task_url_is_resolved(self):
        url = reverse('delete-task')
        self.assertEquals(resolve(url).func, delete_task)