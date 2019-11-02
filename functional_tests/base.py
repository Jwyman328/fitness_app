from selenium import webdriver 
from selenium.webdriver.common.keys import Keys


from django.test.testcases import LiveServerTestCase
from django.test.testcases import TestCase
from users.models import My_custom_user

import time

from unittest import skip

site = "joejoewhitewillysite.xyz"

class Test_base(LiveServerTestCase):
    
    def setUp(self):
        self.browser = webdriver.Chrome()
        #self.browser = browser.get('http://joejoewhitewillysite.xyz/accounts/login/')
        self.user = My_custom_user.objects.create_superuser(
            username="admin",
            password="adminadmin",
            email="admin@example.com")

        self.client.force_login(self.user)
        time.sleep(3)
        self.client.get('/accounts/login/')

    def tearDown(self):
        self.browser.quit()

    def auto_login(self, username='admin', password='adminadmin'):
        self.browser.get(self.live_server_url)
        # the user then find the Login button and clicks it
        self.browser.find_element_by_id('login').click()

        #check that the login_url matches the new_url
        #explicait wait 
        time.sleep(.5)
        login_url = self.browser.current_url
        username_input_box = self.browser.find_element_by_name('username')
        pass_word_input_box = self.browser.find_element_by_name('password')

        #the user then puts in his password and username 
        username_input_box.send_keys(username)
        pass_word_input_box.send_keys(password)
        pass_word_input_box.send_keys(Keys.ENTER)
        time.sleep(.3)

    def auto_input_data(
            self, date_input, sleep_input, workout_intensity_input,
            workout_time_input, steps_input ):
        #auto_login must already have been called 
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
        date_box.send_keys(date_input) #use the current date auto input 
        
        sleep_box.clear()
        sleep_box.send_keys(sleep_input) #5

        water_100oz_box.click()
        clean_eating_box.click()

        workout_intensity_box.clear()
        workout_intensity_box.send_keys(workout_intensity_input)

        workout_time_box.clear()
        workout_time_box.send_keys(workout_time_input) #60

        steps_box.clear()
        steps_box.send_keys(steps_input) #10000
        steps_box.send_keys(Keys.ENTER) #hit enter for all items to enter

        time.sleep(.5) #total points is 82

    def auto_create_user(self):
        self.user_2 = My_custom_user.objects.create_superuser(
            username="admin2",
            password="adminadmin2",
            email="admin@example2.com")
    
    def auto_log_out(self):
        # user decides to log out 
        self.browser.find_element_by_id('account').click()
        self.browser.find_element_by_id('logout').click()
        time.sleep(.3)