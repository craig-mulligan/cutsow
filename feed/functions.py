from django.contrib import messages
from django.db.models import Sum

import uuid
from django.core.cache import cache

def unique_key():
    key = uuid.uuid4()
    if cache.get(key):
        return unique_key
    return key