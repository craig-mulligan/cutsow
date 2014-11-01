from django.db import models
from django.contrib.auth.models import User
import datetime

class Product(models.Model):
    title = models.TextField(default=None, null=True)
    description = models.TextField(default=None, null=True)
    rating = models.IntegerField(default=0)
    user = models.ForeignKey(User)
    image = models.ImageField(upload_to = 'static/product_images/', default = 'product_images/no-img.jpg')

    @classmethod
    def create(cls):
        return cls(completed=datetime.datetime.utcnow())