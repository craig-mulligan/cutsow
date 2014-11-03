from django.db import models
from django.contrib.auth.models import User
import datetime

class Product(models.Model):
    created = models.DateTimeField(default=datetime.datetime.utcnow())
    title = models.TextField(default=None, null=True)
    description = models.TextField(default=None, null=True)
    user = models.ForeignKey(User)
    rating = models.IntegerField(default=0)
    image = models.ImageField(upload_to = 'static/product_images/', default = 'product_images/no-img.jpg')
    dopers = models.ManyToManyField(User, related_name='dopers', symmetrical=False, blank=True)
    
