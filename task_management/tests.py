from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from task_management.models import Task


class TaskManagementTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.client.login(username='testuser', password='testpass123')

    def test_create_task(self):
        response = self.client.post(reverse('create_task'), {
            'title': 'Test Task',
            'description': 'This is a test task',
            'due_date': datetime.now() + timedelta(days=1),
            'owner': self.user.id
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Task.objects.filter(title='Test Task').exists())

    def test_mark_task_complete(self):
        task = Task.objects.create(
            title='Test Task',
            description='Test description',
            due_date=datetime.now() + timedelta(days=1),
            creator=self.user,
            owner=self.user
        )
        response = self.client.post(reverse('mark_task_complete', args=[task.id]))
        self.assertEqual(response.status_code, 302)
        updated_task = Task.objects.get(id=task.id)
        self.assertTrue(updated_task.completed)
