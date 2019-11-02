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

class Test_rules(Test_base):
    
    def test_rules_page(self):
        #user clicks on rules link
        self.auto_login()
        self.browser.find_element_by_id('rules_page').click()
        #user sees rules page
        self.assertIn('rules', self.browser.current_url)
        point_title = self.browser.find_element_by_id('rules_title').text
        self.assertEqual('How to Earn Points', point_title)
        
