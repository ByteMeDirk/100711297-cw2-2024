from django.contrib.auth.models import User
from django.db import models


class Event(models.Model):
    """
    Event Model that represents an event in the calendar.
    """

    title = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
