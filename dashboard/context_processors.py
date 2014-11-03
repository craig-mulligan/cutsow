from feed import models
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

def notificationcount_processor(request):
	    notificationscount = models.Notification.objects.filter(recipient=request.user.id).filter(notified = False).count()   
	    if notificationscount > 0:
	    	return {'notificationscount': notificationscount}
	    else:
	    	return {'notificationscount': False }

