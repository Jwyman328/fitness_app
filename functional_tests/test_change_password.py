from selenium import webdriver 
from selenium.webdriver.common.keys import Keys


from django.test.testcases import LiveServerTestCase
from django.test.testcases import TestCase

from users.models import My_custom_user

from .base import Test_base

import time
from unittest import skip

class Test_change_password(Test_base):

    def test_can_change_password(self):
        # a user logs in 
        self.auto_login()
        #user goes to change password page 
        self.browser.find_element_by_id('account').click()
        self.browser.find_element_by_id('change_password').click()
        self.assertIn('accounts/password_change/', self.browser.current_url)
        
        old_password_box = self.browser.find_element_by_name('old_password')
        new_password_box = self.browser.find_element_by_name('new_password1')
        confirmation_password_box = self.browser.find_element_by_name('new_password2')

        old_password_box.send_keys('adminadmin')
        new_password_box.send_keys('different_password123!')
        confirmation_password_box.send_keys('different_password123!')
        new_password_box.send_keys(Keys.ENTER)
        # user is brought to the confirmation page 
        self.assertIn('/accounts/password_change/done/', self.browser.current_url)
        #user logs out 
        self.auto_log_out()
        #user logs back in
        self.auto_login(username='admin', password='different_password123!')
        # user sees they have logged back in
        user_name_label = self.browser.find_element_by_id('user_name_label').text
        self.assertEqual(user_name_label, 'admin')



