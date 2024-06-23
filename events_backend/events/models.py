from django.contrib.auth.models import User
from django.db import models


class Event(models.Model):
    objects = None
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=200)
    capacity = models.IntegerField()
    available_seats = models.IntegerField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_events')
    attendees = models.ManyToManyField(User, related_name='attended_events', blank=True)
    image = models.ImageField(upload_to='images_events', blank=True)

    def __str__(self):
        return self.title


class Attendance(models.Model):
    objects = None
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    attendee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='event_attendances')
    date_registered = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('event', 'attendee')

    def __str__(self):
        return f'{self.attendee.username} registered for {self.event.title}'
