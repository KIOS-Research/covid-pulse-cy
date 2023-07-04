"""djangotemp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import include, path, re_path
from django.contrib.auth.views import LoginView
from pulseapp import forms
from pulseapp import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import settings
from django.contrib.staticfiles import views as viewsstatic
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LoginView.as_view(authentication_form=forms.OTPAuthenticationForm), name="login"),
    path('', include('pulseapp.urls', namespace="pulseapp")),
    path('logout/', views.logoutUser, name="logout"),
]
if settings.DEBUG:
    urlpatterns += [
        re_path(r'^staticfiles/(?P<path>.*)$', viewsstatic.serve),
    ]