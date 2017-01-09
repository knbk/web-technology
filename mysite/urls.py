from django.conf.urls import url, include
from django.contrib import admin
from rest_framework_swagger.views import get_swagger_view


schema_view = get_swagger_view(title='Lyrics API')

urlpatterns = [
    url(r'', include('lyrics.urls')),
    url(r'^api/', include('lyrics.api')),
    url(r'^api-docs/$', schema_view, 'docs'),
    url(r'^api-auth/', include('rest_framework.urls')),
    url(r'^api/docs/', include('rest_framework_docs.urls')),
    url(r'^admin/', admin.site.urls),
]
