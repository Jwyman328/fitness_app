"""papaginos URL Configuration

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
from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('set_goals',views.Set_goals_view.as_view(), name='set_goal'),
    path('see_goals', views.See_goals_view.as_view(), name='see_goals'),
    path('past_goals', views.Past_goals.as_view(), name='past_goals'),
    path('delete_goal/<int:pk>/', views.Delete_goal.as_view(), name='delete_goal'),
]
