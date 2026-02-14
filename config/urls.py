"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from . import views as config_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', config_views.public_home, name='home'),
    path('debug/403/', config_views.preview_403, name='debug_403'),
    path('debug/404/', config_views.preview_404, name='debug_404'),
    path('accounts/', include('accounts.urls')),
    path('students/', include('students.urls')),
    path('teachers/', include('teachers.urls')),
    path('formations/', include('formations.urls')),
    path('courses/', include('courses.urls')),
    path('grades/', include('grades.urls')),
    path('dashboard/', include('dashboard.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler403 = "config.views.custom_403"
handler404 = "config.views.custom_404"
