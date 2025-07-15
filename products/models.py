from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
import secrets
from datetime import timedelta

User = get_user_model()

def generate_consumer_key():
    return secrets.token_urlsafe(32)

def generate_consumer_secret():
    return secrets.token_urlsafe(64)

class App(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=100, unique=True)
    consumer_key = models.CharField(max_length=100, default=generate_consumer_key)
    consumer_secret = models.CharField(max_length=200, default=generate_consumer_secret)
    is_sandbox = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class AccessToken(models.Model):
    product = models.ForeignKey(App, on_delete=models.CASCADE)
    token = models.CharField(max_length=128, unique=True, default=secrets.token_urlsafe)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    revoked = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(hours=1)
        super().save(*args, **kwargs)

    def is_expired(self):
        return timezone.now() >= self.expires_at
