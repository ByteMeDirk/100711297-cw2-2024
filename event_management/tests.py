import json
from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from event_management.models import Event


class EventManagementTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.client.login(username='testuser', password='testpass123')

    def test_create_event(self):
        # Convert datetime objects to strings and use json.dumps() to format the data
        data = json.dumps({
            'title': 'Test Event',
            'description': 'This is a test event',
            'start': datetime.now().isoformat(),
            'end': (datetime.now() + timedelta(hours=2)).isoformat()
        })
        response = self.client.post(reverse('add_event'), data, content_type='application/json')  # Specify content_type
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Event.objects.filter(title='Test Event').exists())

    def test_update_event(self):
        event = Event.objects.create(
            title='Original Event',
            description='Original description',
            start_time=datetime.now(),
            end_time=datetime.now() + timedelta(hours=1),
            owner=self.user
        )
        # Convert datetime objects to strings and use json.dumps() to format the data
        data = json.dumps({
            'title': 'Updated Event',
            'description': 'Updated description',
            'start': datetime.now().isoformat(),
            'end': (datetime.now() + timedelta(hours=2)).isoformat()
        })
        response = self.client.post(reverse('update_event', args=[event.id]), data,
                                    content_type='application/json')  # Specify content_type
        self.assertEqual(response.status_code, 200)
        updated_event = Event.objects.get(id=event.id)
        self.assertEqual(updated_event.title, 'Updated Event')
