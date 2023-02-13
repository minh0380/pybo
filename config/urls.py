"""config URL Configuration

The `urlpatterns` list routes URLs to views2. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views2
    1. Add an import:  from my_app import views2
    2. Add a URL to urlpatterns:  path('', views2.home, name='home')
Class-based views2
    1. Add an import:  from other_app.views2 import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from pybo.views import base_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('pybo/', include('pybo.urls')),
    path('common/', include('common.urls')),
    path('', base_views.index, name='index'), # '/'에 해당되는 path
]
