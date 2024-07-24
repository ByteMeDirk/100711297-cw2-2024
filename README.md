# 100711297-cw2-2024

Coursework 2 Code Assignment 2024

Based on the provided Django project code, I'll create a comprehensive testing strategy document that includes unit
tests and other SDLC test plans. This document will ensure thorough testing of the developed solution.

## Testing Strategy Document for Beecham Family App

### 1. Introduction

This document outlines the testing strategy for the Beecham Family App, a Django-based web application for managing
events and tasks. The strategy covers various testing phases and methodologies to ensure the quality and reliability of
the application.

### 2. Testing Objectives

- Verify the functionality of all features
- Ensure data integrity and security
- Validate user interface and user experience
- Confirm compatibility across different browsers and devices
- Assess performance and scalability

### 3. Testing Levels

#### 3.1 Unit Testing

Unit tests will be written for individual components and functions using Django's built-in testing framework. Here are
some example unit tests for the project:

```python
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import datetime, timedelta
from event_management.models import Event
from task_management.models import Task


class UserAuthenticationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')

    def test_user_login(self):
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'testpass123'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))

    def test_user_registration(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'newpass123',
            'password2': 'newpass123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())


class EventManagementTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.client.login(username='testuser', password='testpass123')

    def test_create_event(self):
        response = self.client.post(reverse('add_event'), {
            'title': 'Test Event',
            'description': 'This is a test event',
            'start_time': datetime.now(),
            'end_time': datetime.now() + timedelta(hours=2)
        })
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
        response = self.client.post(reverse('update_event', args=[event.id]), {
            'title': 'Updated Event',
            'description': 'Updated description',
            'start': datetime.now().isoformat(),
            'end': (datetime.now() + timedelta(hours=2)).isoformat()
        })
        self.assertEqual(response.status_code, 200)
        updated_event = Event.objects.get(id=event.id)
        self.assertEqual(updated_event.title, 'Updated Event')


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
```

#### 3.2 Integration Testing

Integration tests will focus on the interaction between different components of the application, such as:

- User authentication and authorization
- Event creation and calendar integration
- Task creation and assignment
- Data flow between different modules

#### 3.3 System Testing

System testing will evaluate the entire application as a whole, including:

- End-to-end user workflows
- Data consistency across different features
- Performance under various load conditions
- Security and access control

#### 3.4 User Acceptance Testing (UAT)

UAT will involve real users testing the application to ensure it meets their requirements and expectations.

### 4. Test Environment

- Development: Local machines with Django development server
- Staging: Dedicated server mimicking production environment
- Production: Live server with real user data

### 5. Testing Tools

- Django TestCase for unit and integration testing
- Selenium for automated UI testing
- JMeter for performance testing
- OWASP ZAP for security testing

### 6. Test Cases

Detailed test cases will be developed for each feature, including:

- User registration and authentication
- Event creation, editing, and deletion
- Task management and assignment
- Calendar view and interactions
- User profile management

### 7. Bug Tracking and Reporting

- Use a bug tracking system (e.g., JIRA) to log and manage issues
- Include steps to reproduce, expected vs. actual results, and severity levels

### 8. Performance Testing

- Simulate concurrent users accessing the application
- Measure response times for critical operations
- Identify bottlenecks and optimize as needed

### 9. Security Testing

- Perform vulnerability scans
- Test for common web application security issues (e.g., XSS, CSRF, SQL injection)
- Verify proper implementation of authentication and authorization

### 10. Compatibility Testing

- Test on different web browsers (Chrome, Firefox, Safari, Edge)
- Verify responsiveness on various devices (desktop, tablet, mobile)

### 11. Regression Testing

- Conduct regression tests after each significant change or bug fix
- Automate critical test cases for efficient regression testing

### 12. Test Schedule and Milestones

- Unit Testing: Ongoing throughout development
- Integration Testing: Weekly
- System Testing: Bi-weekly
- UAT: Prior to each release
- Performance and Security Testing: Monthly

### 13. Roles and Responsibilities

- Developers: Write and maintain unit tests
- QA Team: Conduct integration, system, and UAT testing
- Security Team: Perform security audits and penetration testing
- Project Manager: Oversee testing process and report progress

### 14. Exit Criteria

- All critical and high-priority bugs resolved
- 95% of test cases passed
- Performance benchmarks met
- UAT sign-off received

### 15. Risks and Mitigation

- Identify potential risks (e.g., tight deadlines, resource constraints)
- Develop mitigation strategies for each identified risk

By implementing this comprehensive testing strategy, we can ensure the Beecham Family App is thoroughly tested and meets
the required quality standards before deployment.
