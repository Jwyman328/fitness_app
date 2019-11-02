from selenium import webdriver 
from selenium.webdriver.common.keys import Keys


from django.test.testcases import LiveServerTestCase
from django.test.testcases import TestCase

from users.models import My_custom_user

from .base import Test_base

import time
from unittest import skip

site = "joejoewhitewillysite.xyz"

class Test_homepage(Test_base):
    
    def test_login(self):
        # a user goes to the site home page 
        self.browser.get(self.live_server_url)
        # the user then find the Login button and clicks it
        self.browser.find_element_by_id('login').click()

        #check that the login_url matches the new_url
        #explicait wait 
        time.sleep(.5)
        login_url = self.browser.current_url
        self.assertIn('/accounts/login/', login_url )
        username_input_box = self.browser.find_element_by_name('username') 
        pass_word_input_box = self.browser.find_element_by_name('password')

        #the user then puts in his password and username 
        username_input_box.send_keys("admin")
        pass_word_input_box.send_keys("adminadmin")
        pass_word_input_box.send_keys(Keys.ENTER)
        time.sleep(3)
        # assert that the user has entered there account
        user_name_label = self.browser.find_element_by_id('user_name_label').text
        self.assertEqual(user_name_label, 'admin')
    
    def test_log_out(self):
        # a user goes to log in
        self.auto_login()
        # user decides to log out 
        self.browser.find_element_by_id('account').click()
        self.browser.find_element_by_id('logout').click()
        time.sleep(3)
        # the user sees they are back at the login page 
        self.assertIn('/accounts/login/', self.browser.current_url)

    def test_health_data_input_is_converted_correctly(self):
        pass




    




        
        
        


