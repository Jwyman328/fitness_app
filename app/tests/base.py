from django.test.testcases import TestCase, Client
from django.test.client import RequestFactory
from django.contrib.auth.models import AnonymousUser, User
from django.core.exceptions import ValidationError

from ..forms import Point_goals_form, Health_input_form 
from ..models import Point_goals
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

        self.health_input_data = {'date':'2019-03-28', 'Hours_of_sleep': 5,
            'Water_100oz': True, 'clean_eating': False, 'workout_intensity': 3,
            'workout_amount_of_time':60, 'steps': 10000}

        self.invalid_health_input_data= {'date':'2019-03-28', 'Hours_of_sleep': 'ten',
            'Water_100oz': True, 'clean_eating': False, 'workout_intensity': 3,
            'workout_amount_of_time':60, 'steps': 10000}

    def health_input_to_point_conversion(self, health_input_data={}):
        #create and return new dictionary of the health_model_points
        health_model_points = {}
        health_model_points['sleep_points'] = int(health_input_data['Hours_of_sleep'] * 3.3)
        health_model_points['workout_points'] = int(health_input_data['workout_intensity'] * (health_input_data['workout_amount_of_time'] * .2))
        health_model_points['step_points'] = int(health_input_data['steps'] * .001)
        # calculate clena_eating_points based off bolean 
        if health_input_data['clean_eating'] == True:
            health_model_points['clean_eating_points'] = 10
        else:
            health_model_points['clean_eating_points'] = 0
        # calculate water_points based off bolean
        if health_input_data['Water_100oz'] == True:
            health_model_points['water_points'] = 10
        else:
            health_model_points['water_points'] = 0

        #calculate total_points
        total_points = 0
        for key, value in health_model_points.items():
            total_points += value
        health_model_points['total_points'] = int(total_points)
         
        return health_model_points


        
        

        

