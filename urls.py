from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login, logout, password_reset_done, password_reset, password_reset_confirm, password_reset_complete
from django.contrib import admin
import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
admin.autodiscover()


urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^register/$', views.register),
                       url(r'^confirm/(?P<key>.*)$', views.confirm),
                       url(r'^feed/', include('feed.urls')),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^profile/$', views.profile, name='profile'),
                       url(r'^login/$',  login),
                       url(r'^resetpassword/passwordsent/$', password_reset_done),
                       url(r'^resetpassword/$', password_reset),
                       url(r'^reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', password_reset_confirm),
                       url(r'^reset/done/$', password_reset_complete),
                       url(r'^logout/$', views.logout_view),
                       url(r'^/', include('django.contrib.auth.urls')),
                       )
urlpatterns += staticfiles_urlpatterns()