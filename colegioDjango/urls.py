from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponseNotFound
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('myColegioDjango.urls')),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
