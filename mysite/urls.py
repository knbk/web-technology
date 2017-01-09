from django.conf.urls import url, include
from django.contrib import admin


urlpatterns = [
    url(r'', include('lyrics.urls')),
    url(r'^api/', include('lyrics.api')),
    url(r'^api-auth/', include('rest_framework.urls')),
    url(r'^api/docs/', include('rest_framework_docs.urls')),
    url(r'^admin/', admin.site.urls),
]
