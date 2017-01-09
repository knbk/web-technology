from django.conf.urls import url
from . import views
import django.contrib.auth.views


urlpatterns = [
    url(r'^login/$', django.contrib.auth.views.login, name='login'),
    url(r'^logout/$', django.contrib.auth.views.logout, name='logout', kwargs={'next_page': '/'}),
    url(r'^register/$', views.register, name='register'),
]
