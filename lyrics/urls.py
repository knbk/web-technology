from django.conf.urls import url

from lyrics.views import home


app_name = 'lyrics'
urlpatterns = [
    url(r'^$', home, name='home'),
]
