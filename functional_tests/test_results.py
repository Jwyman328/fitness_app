from selenium import webdriver 
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select

from django.test.testcases import LiveServerTestCase
from django.test.testcases import TestCase

from users.models import My_custom_user

from .base import Test_base

import time
from unittest import skip

class Test_results(Test_base):

    def auto_check_results_table(self, desired_sleep_points, desired_date, 
        desired_water_points,desired_clean_eating_points, 
        desired_workout_points, desired_step_points, desired_total_points, desired_point_goal='0'):
        # once a user is already on the results table page they can call this function
        total_points = self.browser.find_element_by_id('total_points').text
        point_goal = self.browser.find_element_by_id('point_goal').text
        workout_points = self.browser.find_element_by_id('workout_points').text
        sleep_points = self.browser.find_element_by_id('sleep_points').text
        water_points = self.browser.find_element_by_id('water_points').text
        step_points = self.browser.find_element_by_id('step_points').text
        clean_eating_points = self.browser.find_element_by_id('clean_eating_points').text
        update_link = self.browser.find_element_by_id('update')
        see_graph_link = self.browser.find_element_by_id('see_graph')

        self.assertEqual(total_points, desired_total_points)
        self.assertEqual(point_goal, desired_point_goal)
        self.assertEqual(workout_points, desired_workout_points)
        self.assertEqual(sleep_points, desired_sleep_points)
        self.assertEqual(water_points, desired_water_points)
        self.assertEqual(step_points, desired_step_points)
        self.assertEqual(clean_eating_points, desired_clean_eating_points)

    def auto_update_input_data(self):
        #the user is already at the updatepage and they then update the data 
        date = self.browser.find_element_by_name('date')
        Hours_of_sleep = self.browser.find_element_by_name('Hours_of_sleep')
        water_points = self.browser.find_element_by_id('id_Water_100oz')
        clean_eating = self.browser.find_element_by_id('id_clean_eating')
        workout_intensity = self.browser.find_element_by_name('workout_intensity')
        workout_time = self.browser.find_element_by_name('workout_amount_of_time')
        steps = self.browser.find_element_by_name('steps')
        #input in all new data 
        ###date.clear()
        ###date.send_keys('2019-03-03') doesnt work to change the date 
        Hours_of_sleep.clear()
        Hours_of_sleep.send_keys('8')
        water_points.click() #click so water is ticked off 
        clean_eating.click() #click so clean eating is ticker off 
        workout_intensity.clear()
        workout_intensity.send_keys('1') 
        workout_time.clear()
        workout_time.send_keys('30')
        steps.clear()
        steps.send_keys('5000')
        #user hits enter 
        steps.send_keys(Keys.ENTER)

    def test_daily_table_page(self):
        #user logs in
        self.auto_login()
        #user inputs data
        self.auto_input_data('2019-03-28','5','3','60','10000')
        #user goes to the Daily Point data page
        self.browser.find_element_by_id('view_results').click()
        self.browser.find_element_by_id('results_daily_table').click()
        
        self.assertIn('daily_point_date_list', self.browser.current_url)
        # user sees the inputted data in the table 
        self.auto_check_results_table('16', 'Mar. 28, 2019','10','10','36','10','82')
        update_link = self.browser.find_element_by_id('update')
        see_graph_link = self.browser.find_element_by_id('see_graph')

  

    def test_see_graph_page_exists(self):
         #user logs in
        self.auto_login()
        #user inputs data
        self.auto_input_data('2019-03-28','5','3','60','10000')
        #user goes to the Daily Point data page
        self.browser.find_element_by_id('view_results').click()
        self.browser.find_element_by_id('results_daily_table').click()
        see_graph_link = self.browser.find_element_by_id('see_graph')
        see_graph_link.click()
        #user arrives at graph page 
        self.assertIn('graphs/daily_point_graph',self.browser.current_url)

    def test_update_health_data_from_table_view(self):
                 #user logs in
        self.auto_login()
        #user inputs data
        self.auto_input_data('2019-03-28','5','3','60','10000')
        #user goes to the Daily Point data page
        self.browser.find_element_by_id('view_results').click()
        self.browser.find_element_by_id('results_daily_table').click()
        # user clicks update link
        update_link = self.browser.find_element_by_id('update').click()
        # user arrives at update page
        self.assertIn('daily_input_update',self.browser.current_url)
        #user updates the health data 
        self.auto_update_input_data() 
        
        #user gets sent to the graph page 
        self.assertIn('daily_point_graph', self.browser.current_url)
        # user navigates to the results table 
        self.browser.find_element_by_id('view_results').click()
        self.browser.find_element_by_id('results_daily_table').click()
        #user checks that the data has been changed to the updated data 
        self.auto_check_results_table('26', 'Mar. 28, 2019','0','0','6','5','37')

    def test_update_health_data_from_graph_view(self):
        #user logs in
        self.auto_login()
        #user inputs data
        self.auto_input_data('2019-03-28','5','3','60','10000')
        #user goes to the Daily Point data page
        self.browser.find_element_by_id('view_results').click()
        self.browser.find_element_by_id('results_daily_table').click()
        see_graph_link = self.browser.find_element_by_id('see_graph')
        see_graph_link.click()
        self.assertIn('daily_point_graph', self.browser.current_url)
        # user clicks on update link and is sent to update page 
        self.browser.find_element_by_id('update_health_data').click()
        self.assertIn('daily_input_update',self.browser.current_url)
        self.auto_update_input_data() #health input data is updated 
        
        #user gets sent to the graph page 
        self.assertIn('daily_point_graph', self.browser.current_url)
        # user navigates to the results table 
        self.browser.find_element_by_id('view_results').click()
        self.browser.find_element_by_id('results_daily_table').click()
        #user checks that the data has been changed to the updated data 
        self.auto_check_results_table('26', 'Mar. 28, 2019','0','0','6','5','37')

        



        


