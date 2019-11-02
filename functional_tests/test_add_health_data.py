
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys


from django.test.testcases import LiveServerTestCase
from django.test.testcases import TestCase

from users.models import My_custom_user

from .base import Test_base

import time
from unittest import skip



class Test_add_health_data(Test_base):
    
    def test_can_input_points_add_health_data(self):
        self.auto_login()
        # a user is logged and clicks input points 
        self.browser.get(self.live_server_url) 
        time.sleep(.5)
        input_points_button = self.browser.find_element_by_id('input_points').click()
        time.sleep(.5)
        # the user arrives to the add_health_data page 
        self.assertIn('add_health_data', self.browser.current_url)
        # user then inputs all required data 
        date_box = self.browser.find_element_by_name('date')
        sleep_box = self.browser.find_element_by_name('Hours_of_sleep')
        water_100oz_box = self.browser.find_element_by_name('Water_100oz')
        clean_eating_box = self.browser.find_element_by_name('clean_eating')
        workout_intensity_box = self.browser.find_element_by_name('workout_intensity')
        workout_time_box = self.browser.find_element_by_name('workout_amount_of_time') # may be workout_amount_of_time
        steps_box = self.browser.find_element_by_name('steps')
        
        date_box.clear()
        date_box.send_keys('2019-03-28') #use the current date auto input 
        
        sleep_box.clear()
        sleep_box.send_keys('5')

        water_100oz_box.click()
        clean_eating_box.click()

        workout_intensity_box.clear()
        workout_intensity_box.send_keys('3')

        workout_time_box.clear()
        workout_time_box.send_keys('60')

        steps_box.clear()
        steps_box.send_keys('10000')
        steps_box.send_keys(Keys.ENTER) #hit enter for all items to enter

        time.sleep(.5)
        # the user gets forwarded to the daily point graph 
        self.assertIn('graphs/daily_point_graph/', self.browser.current_url)
