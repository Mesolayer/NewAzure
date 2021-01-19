# Created with the help of https://www.youtube.com/watch?v=hA_VxnxCHbo

from django.test import TestCase, Client
from django.urls import reverse
from engine.models import *
from datetime import datetime
import json
from django.contrib.auth.models import User
from django.utils.timezone import make_aware


class TestViews(TestCase):    
    def setUp(self):
        self.user = User.objects.create_user(username='dummy',
                                        email='dummy@dummy.com',
                                        password='dummy_for_test_123')

        self.user2 = User.objects.create_user(username='dummy2',
                                         email='dummy2@dummy.com',
                                         password='dummy_for_test_123')

        self.tag1 = Tag.objects.create(user=self.user, name="tag-1")
        self.tag2 = Tag.objects.create(user=self.user2, name="tag-2")

        self.now = make_aware(datetime.now())

        self.task1 = Task.objects.create(user=self.user, 
                                    name='task-1',
                                    start_time_date=self.now,
                                    end_time_date=self.now, 
                                    xp_amount_awarded=10,
                                    is_recurring=False,
                                    comments='task-1-comment',
                                    is_completed=False,
                                    reminder_time_date=self.now)

        self.task2 = Task.objects.create(user=self.user2, 
                                    name='task-2',
                                    start_time_date=self.now,
                                    end_time_date=self.now, 
                                    xp_amount_awarded=20,
                                    is_recurring=False,
                                    comments='task-2-comment',
                                    is_completed=False,
                                    reminder_time_date=self.now)

        self.client = Client()

        self.tag1.tasks.add(self.task1)


    def test_dash_needs_login(self):
        response = self.client.get(reverse('daily-dashboard'))

        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, '/login/?next=/dashboard/daily/')


    def test_dash_GET(self):
        self.client.login(username='dummy', password='dummy_for_test_123')
        response = self.client.get(reverse('daily-dashboard'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'html/dashboard/dashboardwithFullCalenar.html')
        self.assertEquals(response.context.get('title'), 'daily dashboard') 


    def test_dash_GET_tags(self):
        self.client.login(username='dummy', password='dummy_for_test_123')
        response = self.client.get(reverse('daily-dashboard'))

        self.assertEquals(response.context.get('tags')[0].name, 'tag-1')
        self.assertNotIn(self.tag2, response.context.get('tags'))
        self.assertIn(self.tag1, response.context.get('tags'))


    def test_dash_GET_tasks(self):
        self.client.login(username='dummy', password='dummy_for_test_123')
        response = self.client.get(reverse('daily-dashboard'))

        self.assertEquals(response.context.get('tasks')[0].name, 'task-1')
        self.assertNotIn(self.task2, response.context.get('tasks'))
        self.assertIn(self.task1, response.context.get('tasks'))


    def test_dash_filter_tasks(self):
        self.client.login(username='dummy', password='dummy_for_test_123')
        response = json.loads(self.client.get(reverse('dashboard-filter'),
                                                     {'id': self.tag1.pk}).content)

        self.assertEquals(len(response), 1)
        self.assertEquals(response[0].get('title'), self.task1.name)
        self.assertEquals(response[0].get('id'), self.task1.pk)


    def test_create_task_login_required(self):
        response = self.client.get(reverse('create-task'))

        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, '/login/?next=/dashboard/daily/create/')


    def test_create_task_POST(self):
        self.client.login(username='dummy', password='dummy_for_test_123')
        context = {'is_recurring': 'on',
                   'reminder_time_date': '',
                   'start_time_date': '2020-02-15 10:20:30',
                   'end_time_date': '2021-03-20 13:31:59',
                   'name': 'dummy task',
                   'comments': 'bertie4ever'}
        response = self.client.post(reverse('create-task'), context)

        self.assertEquals(response.status_code, 302)
        self.assertEquals(len(Task.objects.filter(user=self.user)), 2)
        task = Task.objects.get(name='dummy task')
        self.assertIsNotNone(task)
        
        # Check that fields were correctly filled in
        start = make_aware(datetime.strptime('2020-02-15 10:20:30', "%Y-%m-%d %H:%M:%S"))
        end = make_aware(datetime.strptime('2021-03-20 13:31:59', "%Y-%m-%d %H:%M:%S"))
        self.assertTrue(task.is_recurring)
        self.assertEquals(start, task.start_time_date)
        self.assertEquals(end, task.end_time_date)
        self.assertEquals(None, task.reminder_time_date)
        self.assertEquals(task.name, 'dummy task')
        self.assertEquals(task.comments, 'bertie4ever')


    def test_assign_tag_login_required(self):
        response = self.client.get(reverse('assign-tag'))

        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, '/login/?next=/dashboard/daily/assign-tag/')


    def test_assign_tag_wrong_user(self):
        self.client.login(username='dummy', password='dummy_for_test_123')
        response = self.client.get(reverse('assign-tag'),
                                          {'tag_id': self.tag1.pk,
                                           'task_id': self.task2.pk})

        self.assertEquals(response.status_code, 401)


    def test_assign_tag_not_exist(self):
        self.client.login(username='dummy', password='dummy_for_test_123')
        response = self.client.get(reverse('assign-tag'),
                                          {'tag_id': 10,
                                           'task_id': self.task1.pk})

        self.assertEquals(response.status_code, 412)

        response = self.client.get(reverse('assign-tag'),
                                          {'tag_id': self.tag1.pk,
                                           'task_id': 10})

        self.assertEquals(response.status_code, 412)


    def test_assign_tag_success(self):
        self.client.login(username='dummy', password='dummy_for_test_123')
        response = self.client.get(reverse('assign-tag'),
                                          {'tag_id': self.tag1.pk,
                                           'task_id': self.task1.pk})

        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(Tag.objects.get(pk=self.tag1.pk).tasks.all()), 1)


    def test_create_tag_login_required(self):
        response = self.client.get(reverse('create-tag'))

        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, '/login/?next=/dashboard/daily/new-tag/')


    def test_create_tag(self):
        self.client.login(username='dummy', password='dummy_for_test_123')
        response = self.client.post(reverse('create-tag'), {'name': 'dummy tag'})

        self.assertEquals(response.status_code, 302)
        tag = list(Tag.objects.all())[-1]
        self.assertEquals(tag.name, "dummy tag")


    def test_complete_task_login_required(self):
        response = self.client.get(reverse('complete-task'))

        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, '/login/?next=/dashboard/daily/complete/')


    def test_complete_task_valid(self):
        self.client.login(username='dummy', password='dummy_for_test_123')
        self.assertFalse(self.task1.is_completed)
        response = self.client.post(reverse('complete-task'), {'id': self.task1.pk})

        self.assertTrue(Task.objects.get(pk=self.task1.pk).is_completed)



    def test_delete_login_required(self):
        response = self.client.get(reverse('delete-task'))

        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, '/login/?next=/dashboard/daily/delete/')


    def test_delete_task_invalid(self):
        self.client.login(username='dummy', password='dummy_for_test_123')
        response = self.client.post(reverse('delete-task'), {'id': -1})
        
        self.assertEquals(len(Task.objects.all()), 2)


    def test_delete_task_wrong_user(self):
        self.client.login(username='dummy', password='dummy_for_test_123')
        response = self.client.post(reverse('delete-task'), {'id': self.task2.pk})
        
        self.assertEquals(len(Task.objects.all()), 2)


    def test_delete_task_valid(self):
        self.client.login(username='dummy', password='dummy_for_test_123')
        response = self.client.post(reverse('delete-task'), {'id': self.task1.pk})
        
        self.assertEquals(len(Task.objects.all()), 1)
        self.assertEquals(Task.objects.all()[0], self.task2)


    def test_update_task_login_required(self):
        response = self.client.get(reverse('update-task'))

        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, '/login/?next=/dashboard/daily/update/')


    def test_update_wrong_user(self):
        self.client.login(username='dummy', password='dummy_for_test_123')
        response = self.client.post(reverse('update-task'), {'is_recurring_editing': "on",
                                                             "id_editing": self.task2.pk})

        self.assertEquals(response.status_code, 302)
        self.assertFalse(self.task2.is_recurring)


    def test_update_recurring(self):
        self.client.login(username='dummy', password='dummy_for_test_123')
        self.assertFalse(Task.objects.get(id=self.task1.pk).is_recurring)

        response = self.client.post(reverse('update-task'), {'is_recurring_editing': "on",
                                                             "id_editing": self.task1.pk,
                                                             "start_time_date_editing": "",
                                                             "end_time_date_editing": "",
                                                             "name_editing": "",
                                                             "comments_editing": "",
                                                             "reminder_time_date_editing": ""})

        self.assertEquals(response.status_code, 302)
        self.assertTrue(Task.objects.get(id=self.task1.pk).is_recurring)


    def test_update_name(self):
        self.client.login(username='dummy', password='dummy_for_test_123')
        self.assertEquals(Task.objects.get(id=self.task1.pk).name, "task-1")

        response = self.client.post(reverse('update-task'), {"id_editing": self.task1.pk,
                                                             "start_time_date_editing": "",
                                                             "end_time_date_editing": "",
                                                             "name_editing": "new-task-1",
                                                             "comments_editing": "",
                                                             "reminder_time_date_editing": ""})

        self.assertEquals(response.status_code, 302)
        self.assertEquals(Task.objects.get(id=self.task1.pk).name, "new-task-1")


    def test_update_start_time_date(self):
        self.client.login(username='dummy', password='dummy_for_test_123')
        self.assertEquals(Task.objects.get(id=self.task1.pk).start_time_date, self.now)

        response = self.client.post(reverse('update-task'), {"id_editing": self.task1.pk,
                                                             "start_time_date_editing": "2020-02-15 10:20:30",
                                                             "end_time_date_editing": "",
                                                             "name_editing": "",
                                                             "comments_editing": "",
                                                             "reminder_time_date_editing": ""})

        self.assertEquals(response.status_code, 302)
        start = make_aware(datetime.strptime('2020-02-15 10:20:30', "%Y-%m-%d %H:%M:%S"))
        self.assertEquals(Task.objects.get(id=self.task1.pk).start_time_date, start)


    def test_update_end_time_date(self):
        self.client.login(username='dummy', password='dummy_for_test_123')
        self.assertEquals(Task.objects.get(id=self.task1.pk).end_time_date, self.now)

        response = self.client.post(reverse('update-task'), {"id_editing": self.task1.pk,
                                                             "start_time_date_editing": "",
                                                             "end_time_date_editing": "2020-02-15 12:20:30",
                                                             "name_editing": "",
                                                             "comments_editing": "",
                                                             "reminder_time_date_editing": ""})

        self.assertEquals(response.status_code, 302)
        end = make_aware(datetime.strptime('2020-02-15 12:20:30', "%Y-%m-%d %H:%M:%S"))
        self.assertEquals(Task.objects.get(id=self.task1.pk).end_time_date, end)


    def test_update_reminder_time_date(self):
        self.client.login(username='dummy', password='dummy_for_test_123')
        self.assertEquals(Task.objects.get(id=self.task1.pk).end_time_date, self.now)

        response = self.client.post(reverse('update-task'), {"id_editing": self.task1.pk,
                                                             "start_time_date_editing": "",
                                                             "end_time_date_editing": "",
                                                             "name_editing": "",
                                                             "comments_editing": "",
                                                             "reminder_time_date_editing": "2020-02-15 12:34:30"})

        self.assertEquals(response.status_code, 302)
        remind = make_aware(datetime.strptime('2020-02-15 12:34:30', "%Y-%m-%d %H:%M:%S"))
        self.assertEquals(Task.objects.get(id=self.task1.pk).reminder_time_date, remind)


    def test_update_comments(self):
        self.client.login(username='dummy', password='dummy_for_test_123')

        response = self.client.post(reverse('update-task'), {"id_editing": self.task1.pk,
                                                             "start_time_date_editing": "",
                                                             "end_time_date_editing": "",
                                                             "name_editing": "",
                                                             "comments_editing": "hello!111",
                                                             "reminder_time_date_editing": ""})

        self.assertEquals(response.status_code, 302)
        self.assertEquals(Task.objects.get(id=self.task1.pk).comments, "hello!111")