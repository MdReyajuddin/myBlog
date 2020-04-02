"""myblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path, include

from posts import views

urlpatterns = [
    path('', views.index, name='index'),
    path('post/<int:id>/', views.post, name='post'),
    path('blog/', views.blog, name='blog'),
    path('search/', views.search, name='search'),
    path('contact/', views.contact, name='contact'),
    path('create/', views.post_create, name='create'),
    path('update/<int:id>/', views.post_update, name='update'),
    path('delete/<int:id>/', views.post_delete, name='delete'),
    path('tinymce/', include('tinymce.urls')),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
