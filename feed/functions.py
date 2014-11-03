from django.contrib import messages
from django.db.models import Max, Min, Sum, F, Count
from feed.models import Notification
import uuid
from django.core.cache import cache

def unique_key():
    key = uuid.uuid4()
    if cache.get(key):
        return unique_key
    return key

def notify(request,recipient, actor, product, text):
	n = Notification.create()
	n.recipient=recipient
	n.text=text
	n.actor=actor
	n.product=product
	n.save()

