from django.contrib import admin
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from feed.models import Info, Notification
from dashboard.models import Product



# Define an inline admin descriptor for Info model
# which acts a bit like a singleton


class InfoInline(admin.StackedInline):
    model = Info
    can_delete = False
    verbose_name_plural = 'info'

# Define a new User admin


class UserAdmin(UserAdmin):
    inlines = (InfoInline, )


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Product)
admin.site.register(Notification)
# Define a new User admin
