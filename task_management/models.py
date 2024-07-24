from django.contrib.auth.models import User
from django.db import models


class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateTimeField()
    completed = models.BooleanField(default=False)

    creator = models.ForeignKey(User, on_delete=models.CASCADE, default=None, related_name='task_creator')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default=None, related_name='task_owner')

    def __str__(self):
        return self.title
