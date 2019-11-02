from django.test.testcases import TestCase, Client
from django.test.client import RequestFactory
from django.contrib.auth.models import AnonymousUser, User
from django.core.exceptions import ValidationError

from users.models import My_custom_user
from goals.views import Set_goals_view

import datetime 
from unittest import skip

from django.contrib.sessions.middleware import SessionMiddleware
    
class TestBase(TestCase):
    def setUp(self):
        # Create a RequestFactory accessible by the entire class.
        self.factory = RequestFactory()
        # Create a new user object accessible by the entire class.
        self.user = My_custom_user.objects.create_user(username='username', 
                                email='footballjoe328@gmail.com', password='password')

        self.goal_data = {'point_goal': 50, 'goal_start_date': '2019-03-28',
            'goal_end_date':'2019-03-30'}

    def auto_client_point_goal_form_creation(self, date_start, date_end, point_goal):
        goal_data = {'point_goal': point_goal, 'goal_start_date': date_start,
            'goal_end_date':date_end}
        self.client.login(username='username', password='password')
        #get/set the session
        session = self.client.session
        session['somekey'] = 'test'
        session.save()
        # get a response with client
        self.response = self.client.post('/goals/set_goals', data =goal_data)
