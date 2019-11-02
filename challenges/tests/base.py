from django.test.testcases import TestCase, Client
from django.test.client import RequestFactory
from django.contrib.auth.models import AnonymousUser, User
from django.core.exceptions import ValidationError
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.sessions.middleware import SessionMiddleware
from ..models import Invitation_to_challenge
from users.models import My_custom_user
from goals.views import Set_goals_view

import datetime 
from unittest import skip

class TestBase(TestCase):
    def setUp(self):
        # Create a RequestFactory accessible by the entire class.
        self.factory = RequestFactory()
        # Create a new user object accessible by the entire class.
        self.user = My_custom_user.objects.create_user(username='username', 
                                email='footballjoe328@gmail.com', password='password')

        self.user_2 = My_custom_user.objects.create_user(username='username_2', 
                                email='footballjoe328@gmail.com', password='password_2')

    def create_invitation_from_user_to_user_2(self):
        self.client.login(username='username', password='password')


        response = self.client.post('/challenges/new_challenge', data={
            'title': 'test_challenge', 'start_date': '2019-03-28', 
            'end_date': '2019-03-30', 'challenge_health_field':'sleep_points', #
            'invitees': str(self.user_2.id) })

    def create_invitation_to_challenge_from_model(self):

        Invitation_to_challenge.objects.create(start_date=datetime.datetime(2019,3,28),
        end_date=datetime.datetime(2019,3,30), challenge_health_field='water_points',
         invitor_user_model=self.user, 
        username_of_invitor=self.user.username, title='test_title')

        # need to user invitees.set() or add cant add it directly for Many2many field
        invitation = Invitation_to_challenge.objects.get(id=1)
        invitation.invitees.add(self.user_2)



