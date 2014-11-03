from django.db import models
from django.contrib.auth.models import User
from dashboard.models import Product
import datetime

class Info(models.Model):
    user = models.OneToOneField(User)
    phone = models.CharField(max_length=255)
    twitter = models.CharField(max_length=255)
    avatar = models.ImageField(upload_to = 'static/avatars/', default = 'avatars/no-img.jpg')
    designer = models.BooleanField(default=False)
    follows = models.ManyToManyField(User, related_name='followed_by', symmetrical=False, blank=True)
    followers = models.ManyToManyField(User, related_name='following', symmetrical=False, blank=True)
    favourites = models.ManyToManyField(Product, related_name='favourites', symmetrical=False, blank=True)

class Notification(models.Model):
    completed = models.DateTimeField()
    notified = models.BooleanField(default=False)
    recipient = models.ForeignKey(User, related_name='recipient')
    text = models.TextField(default=None, null=True)
    actor = models.ForeignKey(User, related_name='actor')
    product = models.ForeignKey(Product, null=True, blank=True)

    @classmethod
    def create(cls):
        return cls(completed=datetime.datetime.utcnow())