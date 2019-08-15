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
from django.urls import path
from . import views 

urlpatterns = [
    path('daily_point_graph/<int:pk>/', views.Daily_point_recap_view.as_view(), name = 'daily_point_graph'), 
    path('User_all_time_progress_graph',views.User_all_time_progress_graph_view.as_view(), name = 'User_all_time_progress_graph'),
    path('daily_points_graph', views.Daily_points_graph_view.as_view(), name = 'daily_points_graph'),
]
