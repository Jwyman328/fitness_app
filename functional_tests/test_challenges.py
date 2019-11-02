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

class Test_challenges(Test_base):

    def auto_create_a_challenge(self):
        # create a second user so they can be invited 
        self.auto_create_user()
        self.auto_login()

        #create a challenge 
        self.browser.find_element_by_id('challenges').click()
        self.browser.find_element_by_id('create_challenge').click()

        title_box = self.browser.find_element_by_name('title')
        start_date_box = self.browser.find_element_by_name('start_date')
        end_date_box = self.browser.find_element_by_name('end_date')

        title_box.send_keys('new challenge')
        start_date_box.clear()
        start_date_box.send_keys('2018-03-28')
        end_date_box.clear()
        end_date_box.send_keys('2050-03-30')
        select = Select(self.browser.find_element_by_name('challenge_health_field'))
        select.select_by_value('water_points')

        time.sleep(.5)
        self.browser.find_element_by_id('id_invitees_1').click() # id of auto created user in invitees list
        time.sleep(.5)
        #user hits enter
        end_date_box.send_keys(Keys.ENTER)
        time.sleep(.3)

    def test_create_a_challenge(self):
        # create a second user so they can be invited
        self.auto_create_user()
        # user logs in
        self.auto_login()
        # user inputs relevant date input data which will later be seen in the leaderboard
        self.auto_input_data('2018-03-29','0','0','0','0') # water points are added automatically
        # user goes to the create challenge page 
        self.browser.find_element_by_id('challenges').click()
        self.browser.find_element_by_id('create_challenge').click()

        #user is sent to the new_challenge page 
        self.assertIn('challenges/new_challenge', self.browser.current_url)
        # user fills out the challenge form
        title_box = self.browser.find_element_by_name('title')
        start_date_box = self.browser.find_element_by_name('start_date')
        end_date_box = self.browser.find_element_by_name('end_date')

        title_box.send_keys('new challenge')
        start_date_box.clear()
        start_date_box.send_keys('2018-03-28')
        end_date_box.clear()
        end_date_box.send_keys('2050-03-30')
        select = Select(self.browser.find_element_by_name('challenge_health_field'))
        select.select_by_value('water_points')

        time.sleep(.5)
        self.browser.find_element_by_id('id_invitees_1').click() # id of auto created user in invitees list
        time.sleep(.5)
        #user hits enter
        end_date_box.send_keys(Keys.ENTER)
        time.sleep(.3)
        # user gets sent to the Accepted_challenges_list page 
        self.assertIn('Accepted_challenges_list', self.browser.current_url)

        #user checks that the data of the challenge is correct
        end_date = self.browser.find_element_by_id('end_date').text
        start_date = self.browser.find_element_by_id('start_date').text
        challenge_title = self.browser.find_element_by_id('challenge_title').text
        challenge_field = self.browser.find_element_by_id('challenge_field').text
        creator = self.browser.find_element_by_id('creator').text
        challenge_leader_board = self.browser.find_element_by_id('challenge_leaderboard')

        self.assertEqual(end_date, 'March 30, 2050')
        self.assertEqual(start_date, 'March 28, 2018')
        self.assertEqual(challenge_title, 'new challenge')
        self.assertEqual(challenge_field, 'water_points')
        self.assertEqual(creator, 'admin')
        self.assertEqual(challenge_leader_board.text, 'LeaderBoard')

        # the user then clicks on the LeaderBoard link to see the leaderboard page 
        challenge_leader_board.click()
        self.assertIn('challenges/challenge_leaderboard/', self.browser.current_url)
        
        #the user sees that they have 10 water_points and there username 
        title = self.browser.find_element_by_id('challenge_title').text
        username = self.browser.find_element_by_id('challenge_username').text
        points = self.browser.find_element_by_id('challenge_points').text
        health_field = self.browser.find_element_by_id('challenge_health_field').text

        self.assertEqual(title, 'Leader Board: new challenge')
        self.assertEqual(username, 'admin')
        self.assertEqual(points, '10')
        self.assertEqual(health_field, 'water_points')

    def test_accept_a_challenge(self):
        #forced_login user created a challenge 
        #inviting admin2
        self.auto_create_a_challenge()
        #forced login user logs out
        self.auto_log_out()
        #admin2 logs in
        self.auto_login(username='admin2', password='adminadmin2')
        user_name_label = self.browser.find_element_by_id('user_name_label').text
        self.assertEqual(user_name_label, 'admin2')

        #user goes to the accept a challenge page
        self.browser.find_element_by_id('challenges').click()
        self.browser.find_element_by_id('pending_invitations').click()
        self.assertIn('challenges/pending_invitations', self.browser.current_url)

        # user sees the current invitation 
        invitation_title = self.browser.find_element_by_id('invitation_title').text
        invitation_start_date = self.browser.find_element_by_id('invitation_start_date').text
        invitation_end_date = self.browser.find_element_by_id('invitation_end_date').text
        invitation_category = self.browser.find_element_by_id('invitation_challenge_category').text
        creator =self.browser.find_element_by_id('invitation_creator').text
        accept_deny_link = self.browser.find_element_by_id('accept_deny_invitation')

        self.assertEqual(invitation_title, 'new challenge')
        self.assertEqual(invitation_start_date,'March 28, 2018' )
        self.assertEqual(invitation_end_date, 'March 30, 2050')
        self.assertEqual(invitation_category, 'water_points')
        self.assertEqual(creator, 'admin')
        self.assertEqual(accept_deny_link.text, 'Accept or reject')

        #user clicks on the accept or reject link
        accept_deny_link.click()
        # user is taken to a new page to update invitation status 
        self.assertIn('update_invitation_status', self.browser.current_url)
        # user selects to accept the invitation 
        select = Select(self.browser.find_element_by_name('status'))
        select.select_by_value('accepted')
        point_on_page = self.browser.find_element_by_id('id_status')
        point_on_page.send_keys(Keys.ENTER)
        #user gets sent back to pending invitations page 
        self.assertIn('pending_invitations', self.browser.current_url)

        #user goes to accepted_challenges page to make sure it was accepted 
        self.browser.find_element_by_id('challenges').click()
        self.browser.find_element_by_id('current_future_challenges').click()
        self.assertIn('challenges/Accepted_challenges_list', self.browser.current_url)
        end_date = self.browser.find_element_by_id('end_date').text
        start_date = self.browser.find_element_by_id('start_date').text
        self.assertEqual(start_date,'March 28, 2018')
        self.assertEqual(end_date,'March 30, 2050')

    def test_reject_challenge_invitation(self):
        self.auto_create_a_challenge()
        self.auto_log_out()

        self.auto_login(username='admin2', password='adminadmin2')
        user_name_label = self.browser.find_element_by_id('user_name_label').text

        #go to challenge pending invitations page 
        self.browser.find_element_by_id('challenges').click()
        self.browser.find_element_by_id('pending_invitations').click()

        # go to accept_deny page
        self.browser.find_element_by_id('accept_deny_invitation').click()
        #user rejects the invitation
        select = Select(self.browser.find_element_by_name('status'))
        select.select_by_value('rejected')
        point_on_page = self.browser.find_element_by_id('id_status')
        point_on_page.send_keys(Keys.ENTER)

        #user gets sent back to pending invitations page 
        self.assertIn('pending_invitations', self.browser.current_url)

        #user goes to accepted_challenges page to make sure it wasn't accepted 
        self.browser.find_element_by_id('challenges').click()
        self.browser.find_element_by_id('current_future_challenges').click()
        self.assertIn('challenges/Accepted_challenges_list', self.browser.current_url)
        
        with self.assertRaises(NoSuchElementException):
            end_date = self.browser.find_element_by_id('end_date').text




        





    
        





        
