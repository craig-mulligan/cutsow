from django.conf.urls import patterns, url, include
import views

urlpatterns = patterns('',
                       url(r'^personal$', views.personal, name='personal'),
                       url(r'^products$', views.products, name='products'),
                       url(r'^following$', views.following, name='following'),
                       url(r'^create$', views.create, name='create'),
                       url(r'^notifications$',views.notifications, name='notifications'),
                       url(r'^favourites$',views.favourites, name='favourites'),
                       url(r'^edit/(?P<product_id>.*)$',views.edit, name='edit'),
                       url(r'^morenotif$',views.loadmoreN, name='morenotif'),
                       )
