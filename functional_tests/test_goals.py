from selenium import webdriver 
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

from django.test.testcases import LiveServerTestCase
from django.test.testcases import TestCase

from users.models import My_custom_user

from .base import Test_base

import time
from unittest import skip

class Test_goals(Test_base):

    def create_a_goal(self, point_goal_input, start_date_input, end_date_input):
        """you need to call auto_login before callign this function """
        # user goes to the set goal page 
        self.browser.find_element_by_id('goals').click() #dropdown goal tab
        self.browser.find_element_by_id('set_goal').click()
        #user inputs goal data 
        point_goal_box = self.browser.find_element_by_name('point_goal')
        start_date_box = self.browser.find_element_by_name('goal_start_date')
        end_date_box = self.browser.find_element_by_name('goal_end_date')

        point_goal_box.clear()
        point_goal_box.send_keys(point_goal_input)
        start_date_box.clear()
        start_date_box.send_keys(start_date_input) # a date that already happened 
        end_date_box.clear()
        end_date_box.send_keys(end_date_input) # a future date 
        end_date_box.send_keys(Keys.ENTER)

    def test_set_goal_input(self):
        # a user logs in
        self.auto_login()

        #user creates a goal
        self.create_a_goal('60', '2019-03-28', '2019-04-28')
        # the user has been routed to the see_goals_page 
        self.assertIn('goals/see_goals', self.browser.current_url)

    def test_current_goal(self):
        # a user logins in
        self.auto_login()
        # user inputs points inside of the goal (to be created)
        self.auto_input_data('2019-03-29','5','3','60','10000')

        # a user goes to the set goal page and inputs a current goal
        self.create_a_goal('60', '2018-03-28', '2050-04-28')

        # the user gets routed to the see goals page and sees all input is correct
        current_total_points_goal = self.browser.find_element_by_id('current_goal_total_point_goal').text
        current_daily_points_goal = self.browser.find_element_by_id('current_goal_daily_point_goal').text
        current_total_points = self.browser.find_element_by_id('current_goal_current_points').text
        current_start_date = self.browser.find_element_by_id('current_goal_start_date').text
        current_end_date = self.browser.find_element_by_id('current_goal_end_date').text
        current_delete = self.browser.find_element_by_id('current_goal_delete').text

        self.assertEqual(current_daily_points_goal, '60')
        self.assertEqual(current_total_points_goal, '703140' ) #60 points for each day between the start - end date
        self.assertEqual(current_total_points, '82') # generate from the data we input 
        self.assertEqual(current_start_date, 'March 28, 2018')
        self.assertEqual(current_end_date, 'April 28, 2050')
        self.assertEqual(current_delete, 'Delete')

    def test_future_goal(self):
        self.auto_login()
       
        # a user goes to the set goal page and inputs a future goal
        self.create_a_goal('60', '2050-03-28', '2050-03-30')

        # the user gets routed to the see goals page and sees all input is correct
        future_total_points_goal = self.browser.find_element_by_id('future_goal_total_point_goal').text
        future_daily_points_goal = self.browser.find_element_by_id('future_goal_daily_point_goal').text
        future_total_points = self.browser.find_element_by_id('future_goal_future_points').text
        future_start_date = self.browser.find_element_by_id('future_goal_start_date').text
        future_end_date = self.browser.find_element_by_id('future_goal_end_date').text
        future_delete = self.browser.find_element_by_id('future_goal_delete').text

        self.assertEqual(future_daily_points_goal, '60')
        self.assertEqual(future_total_points_goal, '120' ) #60 points for each day between the start - end date
        self.assertEqual(future_total_points, '0') # generate from the data we input 
        self.assertEqual(future_start_date, 'March 28, 2050')
        self.assertEqual(future_end_date, 'March 30, 2050')
        self.assertEqual(future_delete, 'Delete')

    def test_delete_a_future_goal(self):
        # user logs in 
        self.auto_login()
        #a user first creates a future goal
        self.create_a_goal('60', '2050-03-28', '2050-03-30')
        # the user sees that the goal exists by finding the start date of the goal 
        future_start_date = self.browser.find_element_by_id('future_goal_start_date').text
        self.assertEqual(future_start_date, 'March 28, 2050')

        # the user then clicks delete
        future_delete = self.browser.find_element_by_id('future_goal_delete').click()
        # user is brought to the delete goal_page 
        self.assertIn('goals/delete_goal/', self.browser.current_url)
        # the user clicks delete on this delete_goal page
        delete_button = self.browser.find_element_by_id('delete')
        delete_button.click()

        # the user is sent back to the see_goals page 
        self.assertIn('see_goals',self.browser.current_url)
        # user now does not see the delete goal on the page 
        with self.assertRaises(NoSuchElementException):
            self.browser.find_element_by_id('future_goal_start_date')

    def test_past_goals_page(self):
        #user logs in
        self.auto_login()
        # a user goes to the set goal page and inputs a pas goal
        self.create_a_goal('60', '2005-03-28', '2005-03-30')
        # user gets sent to the see_goals page 
        self.assertIn('see_goals', self.browser.current_url)
        # user then navigates to the past goals page 
        self.browser.find_element_by_id('goals').click()
        self.browser.find_element_by_id('past_goals').click()
        # user is now at the past goals page 
        self.assertIn('past_goals', self.browser.current_url)
        # user then checks that the goal was created 
        past_total_points_goal = self.browser.find_element_by_id('past_goal_total_point_goal').text
        past_daily_points_goal = self.browser.find_element_by_id('past_goal_daily_point_goal').text
        past_total_points = self.browser.find_element_by_id('past_goal_past_points').text
        past_start_date = self.browser.find_element_by_id('past_goal_start_date').text
        past_end_date = self.browser.find_element_by_id('past_goal_end_date').text
        past_delete = self.browser.find_element_by_id('past_goal_delete').text

        self.assertEqual(past_daily_points_goal, '60')
        self.assertEqual(past_total_points_goal, '120' ) #60 points for each day between the start - end date
        self.assertEqual(past_total_points, '0') # generate from the data we input 
        self.assertEqual(past_start_date, 'March 28, 2005')
        self.assertEqual(past_end_date, 'March 30, 2005')
        self.assertEqual(past_delete, 'Delete')

    






