from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login, logout, password_reset_done, password_reset, password_reset_confirm, password_reset_complete
from django.contrib import admin
import views
admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^feed/$', views.userfeed, name='index'),
                       url(r'^register/$', views.register),
                       url(r'^confirm/(?P<key>.*)$', views.confirm),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^dashboard/', include('dashboard.urls')),
                       url(r'^login/$',  login),
                       url(r'^resetpassword/passwordsent/$', password_reset_done),
                       url(r'^resetpassword/$', password_reset),
                       url(r'^reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', password_reset_confirm),
                       url(r'^reset/done/$', password_reset_complete),
                       url(r'^logout/$', views.logout_view),

                       url(r'^/', include('django.contrib.auth.urls')),
                       url(r'^feed/product/(?P<product_id>.*)$', views.singleproduct, name='product'),
                       url(r'^feed/user/(?P<user_id>.*)$', views.profile, name='profile'),
                       url(r'^feed/followers/user/(?P<user_id>.*)$', views.followerlisting, name='followerlisting'),
                       url(r'^feed/follow/', views.follow, name='follow'),
                       (r'^grappelli/', include('grappelli.urls')),
                       )
