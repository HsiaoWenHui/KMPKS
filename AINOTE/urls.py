"""AINOTE URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from django.urls import path,include
from django.conf import settings
from django.conf.urls import url

from django.views.decorators.csrf import csrf_exempt
from simditor.views import upload_handler

from django.views import generic
from django.conf.urls.static import static
class ImageUploadView(generic.View):
    """ImageUploadView."""

    http_method_names = ['post']

    def post(self, request, **kwargs):
        """Post."""
        return upload_handler(request)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
   
    path('accounts/',include('login.urls')),
    path('personal/',include('personal.urls')),
    path('article/',include('article.urls')),
    path('group/',include('group.urls')),
    # url(r'^markdownx/', include('markdownx.urls')),
    
    url(r'^simditor/upload', csrf_exempt(ImageUploadView.as_view())),
]

urlpatterns += static(
    settings.STATIC_URL,
    document_root=settings.STATIC_ROOT
)

urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)
