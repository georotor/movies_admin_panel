import os
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('movies.api.urls')),
]

if os.environ.get('DEBUG', False) == 'True':
    urlpatterns.append(path('__debug__/', include('debug_toolbar.urls')))
