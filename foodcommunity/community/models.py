from django.db import models
# from django.utils import timezone
from django.contrib.auth.models import User
from django.conf import settings


class Community(models.Model):
    admin = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    topic = models.CharField( max_length=200, null=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="participants", blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.topic


class communitieschat(models.Model):
    topic = models.ForeignKey(Community, on_delete=models.SET_NULL, null=True)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.topic} - {self.sender}: {self.message}"

