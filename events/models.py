from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
import datetime


class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class User(AbstractUser):
    location = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)

    tags = models.ManyToManyField(Tag)

    def upcoming_events(self):
         timezone.now()


class Event(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateTimeField('start date', null=True, blank=True)
    end_date = models.DateTimeField('end date', null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    tags = models.ManyToManyField(Tag, null=True, blank=True)

    organizer = models.ForeignKey(User, related_name='events_organizer_set')
    attendees = models.ManyToManyField(User, related_name='events_attendees_set', null=True, blank=True)

    def __str__(self):
        return self.name
