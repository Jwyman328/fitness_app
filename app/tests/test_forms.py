from django.test.testcases import TestCase, Client
from django.test.client import RequestFactory
from django.contrib.auth.models import AnonymousUser, User
from django.core.exceptions import ValidationError

from .base import TestBase
from ..forms import Point_goals_form, Health_input_form 
from ..models import Point_goals, Point_model, User_point_input_model
from users.models import My_custom_user
from goals.views import Set_goals_view
from users.models import My_custom_user


import datetime 
from unittest import skip

from django.contrib.sessions.middleware import SessionMiddleware

class Test_Point_goals_form(TestBase):

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

    def auto_assert_form_goal_creation(self, date_start=datetime.date(2019,3,28),
            date_end = datetime.date(2019,3,30), point_goal = 50):

        total_points_needed = ( date_end - date_start).days * point_goal
        new_point_goal = Point_goals.objects.get(id=1)
        self.assertEqual(new_point_goal.user, self.user)
        self.assertEqual(new_point_goal.goal_start_date,date_start)
        self.assertEqual(new_point_goal.goal_end_date,date_end)
        self.assertEqual(new_point_goal.point_goal,point_goal)
        self.assertEqual(new_point_goal.points_needed_for_goal_achieved,total_points_needed)
        self.assertEqual(new_point_goal.current_point_total_input, 0)

    def test_point_goals_form_object_create(self):
        """test that a goal model can be created from calling the class form """
        # sign a user in 
        self.client.login(username='username', password='password')
        #get response form form view and test passing
        form = Point_goals_form(user=self.user, data=self.goal_data)
        #response = Set_goals_view(request)
        self.assertTrue(form.is_valid())
        form.save()
        new_point_goal = Point_goals.objects.get(id=1)
        
        self.assertEqual(new_point_goal.goal_start_date, datetime.date(2019,3,28))
        self.assertEqual(new_point_goal.goal_end_date, datetime.date(2019,3,30))
        self.assertEqual(new_point_goal.point_goal, 50)
        self.assertEqual(new_point_goal.points_needed_for_goal_achieved, 100)
        self.assertEqual(new_point_goal.current_point_total_input, 0)

    def test_point_goals_form_form_create(self):
        #login with the client
        self.client.login(username='username', password='password')

        #get/set the session
        session = self.client.session
        session['somekey'] = 'test'
        session.save()

        # get a response with client
        response = self.client.post('/goals/set_goals', data = self.goal_data)
        self.assertEqual(response.status_code, 302)
        self.auto_assert_form_goal_creation()

    def test_invalid_point_goal(self):
        self.client.login(username='username', password='password')
        #get response form form view and test passing
        
        self.client.post('/goals/set_goals', data = {'point_goal': 50, 'goal_start_date': 'not a date',
            'goal_end_date':'2019-03-30'})
        self.assertEqual(Point_goals.objects.count(),0)


class Test_health_input_form(TestBase):

    @skip
    def test_health_input_object(self):
        self.client.login(username='username', password='password')
        my_user = My_custom_user.objects.get(id=1)
        self.assertEqual(my_user, self.user)

        form = Health_input_form(user=self.user, data= self.health_input_data)
        self.assertTrue(form.is_valid())
        form.save() # error the self.user doesnt save

    def test_health_input_post_create_User_point_input_model(self): 
        self.client.login(username='username', password='password')
        #get/set the session
        session = self.client.session
        session['somekey'] = 'test'
        session.save()
        #post the data
        response = self.client.post('/add_health_data', data= self.health_input_data)
        # make sure the data has been created 
        user_point_input_model_created = User_point_input_model.objects.get(id=1)  
        self.assertEqual(user_point_input_model_created.user, self.user)
        self.assertEqual(user_point_input_model_created.date, datetime.date(2019,3,28) )
        self.assertEqual(user_point_input_model_created.Hours_of_sleep,self.health_input_data['Hours_of_sleep'] )
        self.assertEqual(user_point_input_model_created.Water_100oz, self.health_input_data['Water_100oz'] )
        self.assertEqual(user_point_input_model_created.workout_intensity, self.health_input_data['workout_intensity'])
        self.assertEqual(user_point_input_model_created.workout_amount_of_time, self.health_input_data['workout_amount_of_time'] )
        self.assertEqual(user_point_input_model_created.steps, self.health_input_data['steps'] )
        self.assertEqual(user_point_input_model_created.clean_eating, self.health_input_data['clean_eating'] )

    def test_health_input_post_create_point_model(self):
        self.client.login(username='username', password='password')
        #get/set the session
        session = self.client.session
        session['somekey'] = 'test'
        session.save()
        #post the data
        response = self.client.post('/add_health_data', data= self.health_input_data)
        # make sure the data has been created 
        point_model_created = Point_model.objects.get(id=1)  
        #convert the input data to point data 
        health_input_data = self.health_input_to_point_conversion(self.health_input_data)
        # check that the conversion is correct and exists
        # get the related user_point_health_input_object
        user_point_input_model_created = User_point_input_model.objects.get(id=1)
        self.assertEqual(point_model_created.user, self.user)
        self.assertEqual(point_model_created.one_to_one_workout, user_point_input_model_created )
        self.assertEqual(point_model_created.date, datetime.date(2019,3,28) )
        self.assertEqual(point_model_created.sleep_points,health_input_data['sleep_points'] )
        self.assertEqual(point_model_created.water_points, health_input_data['water_points'] )
        self.assertEqual(point_model_created.workout_points, health_input_data['workout_points'])
        self.assertEqual(point_model_created.step_points, health_input_data['step_points'] )
        self.assertEqual(point_model_created.clean_eating_points, health_input_data['clean_eating_points'] )
        self.assertEqual(point_model_created.total_points, health_input_data['total_points'] )

    def test_health_input_invalid_data(self):
        self.client.login(username='username', password='password')
        #get/set the session
        session = self.client.session
        session['somekey'] = 'test'
        session.save()
        #post the data
        response = self.client.post('/add_health_data', data= self.invalid_health_input_data)
        # no input objects created
        self.assertEqual(User_point_input_model.objects.count(), 0)
        # no point model object created
        self.assertEqual(Point_model.objects.count(), 0)

    def test_update_health_data(self):
        """check health data is updated """

        new_input_data = {'date':'2019-03-28', 'Hours_of_sleep': 10,
            'Water_100oz': False, 'clean_eating': True, 'workout_intensity': 1,
            'workout_amount_of_time':30, 'steps': 5000}

        self.client.login(username='username', password='password')
        self.client.post('/add_health_data', data= self.health_input_data)
        self.client.post('/daily_input_update/1/', data=new_input_data)

        user_point_input_model_created = User_point_input_model.objects.get(id=1)  
        self.assertEqual(user_point_input_model_created.user, self.user)
        self.assertEqual(user_point_input_model_created.date, datetime.date(2019,3,28) )
        self.assertEqual(user_point_input_model_created.Hours_of_sleep,new_input_data['Hours_of_sleep'] )
        self.assertEqual(user_point_input_model_created.Water_100oz, new_input_data['Water_100oz'] ) 
        self.assertEqual(user_point_input_model_created.workout_intensity, new_input_data['workout_intensity'])
        self.assertEqual(user_point_input_model_created.workout_amount_of_time, new_input_data['workout_amount_of_time'] )
        self.assertEqual(user_point_input_model_created.steps, new_input_data['steps'] )
        self.assertEqual(user_point_input_model_created.clean_eating, new_input_data['clean_eating'] )
    
    def test_update_health_data_does_not_create_second_object(self):

        new_input_data = {'date':'2019-03-28', 'Hours_of_sleep': 10,
            'Water_100oz': False, 'clean_eating': True, 'workout_intensity': 1,
            'workout_amount_of_time':30, 'steps': 5000}

        self.client.login(username='username', password='password')
        self.client.post('/add_health_data', data= self.health_input_data)
        self.client.post('/daily_input_update/1/', data=new_input_data)
        # count the 
        self.assertEqual(User_point_input_model.objects.count(),1) 

    def test_update_health_data_changes_input__points(self):
        """check point model is updated with health data input update  """

        new_input_data = {'date':'2019-03-28', 'Hours_of_sleep': 10,
            'Water_100oz': False, 'clean_eating': True, 'workout_intensity': 1,
            'workout_amount_of_time':30, 'steps': 5000}

        self.client.login(username='username', password='password')
        self.client.post('/add_health_data', data= self.health_input_data)
        self.client.post('/daily_input_update/1/', data=new_input_data)

        point_model_created = Point_model.objects.get(id=1)  
        #convert the input data to point data 
        health_input_data = self.health_input_to_point_conversion(new_input_data)
        # check that the conversion is correct and exists
        # get the related user_point_health_input_object
        user_point_input_model_created = User_point_input_model.objects.get(id=1)

        self.assertEqual(point_model_created.user, self.user)
        self.assertEqual(point_model_created.one_to_one_workout, user_point_input_model_created )
        self.assertEqual(point_model_created.date, datetime.date(2019,3,28) )
        self.assertEqual(point_model_created.sleep_points,health_input_data['sleep_points'] )
        self.assertEqual(point_model_created.water_points, health_input_data['water_points'] ) 
        self.assertEqual(point_model_created.workout_points, health_input_data['workout_points'])
        self.assertEqual(point_model_created.step_points, health_input_data['step_points'] )
        self.assertEqual(point_model_created.clean_eating_points, health_input_data['clean_eating_points'] )
        self.assertEqual(point_model_created.total_points, health_input_data['total_points'] )









                                  














        


        
        
       
            

        








        
        
