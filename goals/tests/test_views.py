from django.test.testcases import TestCase, Client
from django.test.client import RequestFactory
from django.contrib.auth.models import AnonymousUser, User
from django.core.exceptions import ValidationError

from .base import TestBase

import datetime 
from unittest import skip

from django.contrib.sessions.middleware import SessionMiddleware

class Test_set_goals_view(TestBase):

    def test_set_goal_template_used(self):
        self.client.login(username='username', password='password')
        response = self.client.get('/goals/set_goals')
        self.assertTemplateUsed(response, 'set_goals.html') 

    def test_goal_set_post_redirect(self):
        self.client.login(username='username', password='password')
        response = self.client.post('/goals/set_goals', data=self.goal_data)
        self.assertRedirects(response,'/goals/see_goals')

    #use for checking not logged in 
    def test_non_logged_in_user_cant_access_page(self):
        response = self.client.get('/goals/set_goals')
        self.assertRedirects(response, '/accounts/login/?next=/goals/set_goals')

class Test_see_goals_views(TestBase):
    
    def test_see_goals_template(self):
        self.client.login(username='username', password='password')
        response = self.client.get('/goals/see_goals')
        self.assertTemplateUsed(response, 'see_goal_list.html')

    def test_see_goals_status_code(self):
        self.client.login(username='username', password='password')
        response = self.client.get('/goals/see_goals')
        self.assertEqual(response.status_code, 200)
        
    def test_non_logged_in_user_cant_access_page(self):
        response = self.client.get('/goals/see_goals')
        self.assertRedirects(response, '/accounts/login/?next=/goals/see_goals')

class Test_see_past_goals(TestBase):
    
    def test_see_past_goals_template(self):
        self.client.login(username='username', password='password')
        response = self.client.get('/goals/past_goals')
        self.assertTemplateUsed(response,'past_goal_list.html' )

    def test_see_past_goals_status_code(self):
        self.client.login(username='username', password='password')
        response = self.client.get('/goals/past_goals')
        self.assertEqual(response.status_code, 200)

    def test_non_logged_in_user_cant_access_page(self):
        response = self.client.get('/goals/past_goals')
        self.assertRedirects(response, '/accounts/login/?next=/goals/past_goals')

class Test_delete_goal(TestBase):
    def test_delete_goal_template(self):
        self.client.login(username='username', password='password')
        self.auto_client_point_goal_form_creation('2019-03-28', '2019-03-30', 50)
        response = self.client.get('/goals/delete_goal/1/')
        self.assertTemplateUsed(response,'delete_goal.html' )

    def test_delete_goal_status_code(self):
        self.client.login(username='username', password='password')
        self.auto_client_point_goal_form_creation('2019-03-28', '2019-03-30', 50)
        response = self.client.get('/goals/delete_goal/1/')
        self.assertEqual(response.status_code, 200)


       



