from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
	url(r'', include('app.urls', namespace="app")),
    url(r'^api/', include('api.urls'), ),
    url(r'^admin/', admin.site.urls),
]