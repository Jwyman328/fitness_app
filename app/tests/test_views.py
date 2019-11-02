from django.test.testcases import TestCase, Client
from django.test.client import RequestFactory
from django.contrib.auth.models import AnonymousUser, User
from django.core.exceptions import ValidationError

from .base import TestBase
from ..forms import Point_goals_form, Health_input_form 
from ..models import Point_goals
from users.models import My_custom_user
from goals.views import Set_goals_view

import datetime 
from unittest import skip

from django.contrib.sessions.middleware import SessionMiddleware

# test status codes and templatesused 
class Test_Health_data_input(TestBase):
    
    def test_health_input_form_template(self):
        self.client.login(username='username', password='password')
        #get/set the session
        session = self.client.session
        session['somekey'] = 'test'
        session.save()
        #post the data
        response = self.client.get('/add_health_data')
        self.assertTemplateUsed(response, 'health_data_input_form.html' ) 

    def test_health_input_post_redirects(self):
        self.client.login(username='username', password='password')
        #get/set the session
        session = self.client.session
        session['somekey'] = 'test'
        session.save()

        response = self.client.post('/add_health_data', data= self.health_input_data)
        self.assertRedirects(response, '/graphs/daily_point_graph/1/')
    
    def test_non_logged_in_user_cant_access_page(self):
        response = self.client.get('/add_health_data')
        self.assertRedirects(response, '/accounts/login/?next=/add_health_data')

class Test_Update_health_data_input(TestBase):

    def test_update_health_data_redirect(self):
        self.client.login(username='username', password='password')
        self.client.post('/add_health_data', data= self.health_input_data)
        response = self.client.post('/daily_input_update/1/', data={'date':'2019-03-28', 'Hours_of_sleep': 5,
            'Water_100oz': True, 'clean_eating': False, 'workout_intensity': 3,
            'workout_amount_of_time':60, 'steps': 10000})
        self.assertRedirects(response,'/graphs/daily_point_graph/1/')

    def test_update_health_data_template(self):
        self.client.login(username='username', password='password')
        self.client.post('/add_health_data', data= self.health_input_data)
        response = self.client.get('/daily_input_update/1/')
        
        self.assertTemplateUsed(response, 'update_daily_data_input.html')

    def test_non_logged_in_user_cant_access_page(self):
        response = self.client.get('/daily_input_update/1/')
        self.assertRedirects(response, '/accounts/login/?next=/daily_input_update/1/')


class Test_all_time_leader_board(TestBase):

    def test_all_time_leader_board_template(self):
        self.client.login(username='username', password='password')
        response = self.client.get('/all_time_leader_board')
        self.assertTemplateUsed(response,'all_time_leader_board.html' )

    def test_all_time_leader_board_status_code(self):
        self.client.login(username='username', password='password')
        response = self.client.get('/all_time_leader_board')
        self.assertEqual(response.status_code, 200)

    def test_non_logged_in_user_cant_access_page(self):
        response = self.client.get('/all_time_leader_board')
        self.assertRedirects(response, '/accounts/login/?next=/all_time_leader_board')


class Test_rules(TestBase):

    def test_how_to_template(self):
        response = self.client.get('/rules')
        self.assertTemplateUsed(response, "rules.html")

    def test_how_to_status_code(self):
        response = self.client.get('/rules')
        self.assertEqual(response.status_code, 200)

class How_to(TestBase):
    
    def test_how_to_template(self):
        response = self.client.get('/how_to')
        self.assertTemplateUsed(response, "how_to.html")

    def test_how_to_status_code(self):
        response = self.client.get('/how_to')
        self.assertEqual(response.status_code, 200)

class Daily_point_date_list(TestBase):
    
    def test_daily_point_date_list_template(self):
        self.client.login(username='username', password='password')
        response = self.client.get('/daily_point_date_list')
        self.assertTemplateUsed(response, 'daily_points_date_list.html')

    def test_daily_point_date_list_status_code(self):
        self.client.login(username='username', password='password')
        response = self.client.get('/daily_point_date_list')
        self.assertEqual(response.status_code, 200)

    def test_non_logged_in_user_cant_access_page(self):
        response = self.client.get('/daily_point_date_list')
        self.assertRedirects(response, '/accounts/login/?next=/daily_point_date_list')


