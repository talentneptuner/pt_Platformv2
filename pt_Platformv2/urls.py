"""pt_Platformv2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path, re_path
from django.views.static import serve

from .settings import MEDIA_ROOT

from user.views import LoginView, AdminIndex, UserIndex, LogoutView
from task.views import DistributeTaskView, LabelView, NextView, CloseTaskView
import xadmin

urlpatterns = [
    path('admin/', xadmin.site.urls),
    path('', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('distribute_task/<str:task_id>/', DistributeTaskView.as_view(), name='distribute_task'),
    path('admin_index', AdminIndex.as_view(), name='admin_index'),
    path('user_index', UserIndex.as_view(), name='user_index'),
    path('label/<str:task_id>/', LabelView.as_view(), name='label'),
    path('next', NextView.as_view(), name='next'),
    path('close_task/<str:task_id>/', CloseTaskView.as_view(), name='close_task'),
    re_path('media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT})
]
