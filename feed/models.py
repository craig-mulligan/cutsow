from django.db import models
from django.contrib.auth.models import User


class Info(models.Model):
    user = models.OneToOneField(User)
    phone = models.CharField(max_length=255)
    twitter = models.CharField(max_length=255)
    avatar = models.ImageField(upload_to = 'static/avatars/', default = 'avatars/no-img.jpg')
    rating = models.IntegerField(default=0)
    designer = models.BooleanField(default=False)