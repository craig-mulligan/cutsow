from django.conf.urls import patterns, url
import views
urlpatterns = patterns('',
                       url(r'^personal$', views.personal, name='personal'),
                       url(r'^products$', views.products, name='products'),
                       url(r'^following$', views.following, name='following'),
                       url(r'^create$', views.create, name='create'),
                       url(r'^edit/(?P<product_id>.*)$',views.edit, name='edit'),
                       )
