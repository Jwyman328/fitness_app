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
    path('', views.How_to_view.as_view(), name='home'),
    path(
        'add_health_data', 
         views.Health_data_input.as_view(),
         name='Health_data_input'),
    path(
        'daily_input_update/<int:pk>/',
        views.Update_health_data_input.as_view(),
         name='update_health_data_input'),
    path(
        'daily_point_date_list',
         views.Daily_points_date_list.as_view(),
         name='daily_monthly_points_list'),
    path('all_time_leader_board', 
        views.All_time_leaderboard_view.as_view(),
         name='all_time_leaderboard'),
         
    path('how_to', views.How_to_view.as_view(), name='how_to'),
    path('rules', views.Rules_view.as_view(), name='rules'),
]
