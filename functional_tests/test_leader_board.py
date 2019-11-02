from selenium import webdriver 
from selenium.webdriver.common.keys import Keys


from django.test.testcases import LiveServerTestCase
from django.test.testcases import TestCase

from users.models import My_custom_user

from .base import Test_base

import time
from unittest import skip


class Test_leaderboard_page(Test_base):

    def test_learderboard_displays_results(self):
        #the user logs in and inputs in data 
        self.auto_login()
        self.auto_input_data('2019-03-28','5', '3', '60', '10000') #auto input data already contains an auto_login call

        # user then goes to the Leader Board page 
        self.browser.find_element_by_id('leader_board').click()
        time.sleep(.5)
        #check that the user is on the leaderboard
        username = self.browser.find_element_by_id('username').text
        self.assertEqual(username, 'admin')

        #check the amount of points is correct ()
        total_points = self.browser.find_element_by_id('user_point_total').text
        self.assertEqual(total_points, '82')

      