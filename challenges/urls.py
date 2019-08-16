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
    path('new_challenge', 
          views.Create_a_challenge_view.as_view(),
          name='create_a_challenge'),
    path('pending_invitations',
          views.Accept_deny_challenge_view.as_view(),
          name='invitations_pending'),
    path('update_invitation_status/<int:pk>/',
          views.Update_invitation_status.as_view(),
          name='update_invitation_status'),
    path('Accepted_challenges_list',
          views.Accepted_challenges_view.as_view(),
          name='accepted_challenges_list' ),
    path('past_accepted_challenges',
          views.Past_accepted_challenges.as_view(),
          name='past_accepted_challenges' ),
    path('challenge_leaderboard/<int:pk>/',
          views.Challenge_leaderboard.as_view(),
          name='Challenge_leaderboard'),
]
