from django.contrib.sessions.middleware import SessionMiddleware
from django.test import Client, RequestFactory

from .base import TestBase
from ..models import Challenge, Invitation_to_challenge, Invitation_status
from ..forms import New_challenge_invitation_form
from ..views import Create_a_challenge_view
from users.models import My_custom_user

import datetime

from unittest import skip

class Test_pending_challenges(TestBase):

    def test_pending_challenges_get(self):
        self.client.login(username='username', password='password')
        response = self.client.get('/challenges/pending_invitations')
        self.assertEqual(response.status_code, 200)
    
    def test_pending_challenges_template(self):
        self.client.login(username='username', password='password')
        response = self.client.get('/challenges/pending_invitations')
        self.assertTemplateUsed('accept__deny_challenge.html')


class Test_current_future_accepted_challenges(TestBase):

    def test_current_future_accepted_challenges_status_get(self):
        self.client.login(password='password_2', username='username_2')
        response = self.client.get('/challenges/Accepted_challenges_list')
        self.assertEqual(response.status_code, 200)

    def test_current_future_accepted_challenges_template(self):
        self.client.login(password='password_2', username='username_2')
        response = self.client.get('/challenges/Accepted_challenges_list')
        self.assertTemplateUsed(response, 'Accepted_challenges_list.html')

class Test_past_accepted_challenges(TestBase):
    def test_past_accepted_challenges_status_get(self):
        self.client.login(password='password_2', username='username_2')
        response = self.client.get('/challenges/past_accepted_challenges')
        self.assertEqual(response.status_code, 200)

    def test_past_accepted_challenges_template_used(self):
        self.client.login(password='password_2', username='username_2')
        response = self.client.get('/challenges/past_accepted_challenges')
        self.assertTemplateUsed(response, 'Past_accepted_challenges.html')


class Test_update_invitation_status(TestBase):

    def test_invalid_accept_deny_update_invitation_status_get_404(self):
        """before a challenge is create user should not see page existing """
        self.client.login(username='username', password='password')
        response = self.client.get('/challenges/update_invitation_status/1/')
        self.assertEqual(response.status_code, 404)

    def test_valid_accept_deny_update_invitation_status_get_200(self):
        self.create_invitation_from_user_to_user_2()
        # login in user_2 and go to page 
        self.client.logout()
        self.client.login(password='password_2', username='username_2')
        response = self.client.get('/challenges/update_invitation_status/1/')
        self.assertEqual(response.status_code, 200)

    def test_deny_challenge_invitation(self):
        pass

    @skip
    def test_accept_deny_challenge_accept_redirect(self):
        ## error with the form.instance
        # log out user_1
        self.client.logout()
        # log in user_2
        
        session = self.client.session
        session['somekey'] = 'test'
        session.save()

        self.create_invitation_from_user_to_user_2()
        self.client.logout()
        self.client.login(username='username_2', password='password_2')
        invitation = Invitation_to_challenge.objects.get(id=1)
                
        invitation = Invitation_to_challenge.objects.get(id=1)
        invitation_to_user_2_exists =  Invitation_status.objects.get(id=self.user_2.id) 
        #invitation_to_user_2_exists =  Invitation_status.objects.get(id=self.user_2.id) 
        self.assertEqual(invitation, invitation_to_user_2_exists.invitation)
        self.assertEqual(self.user_2, invitation_to_user_2_exists.invitee) #test that the invitee is user_2

        response = self.client.post('/challenges/update_invitation_status/1/', data={
            'status':'accepted'}, kwargs = {'invitation': invitation })
        
        #self.assertEqual(response.status_code, 302)

class Test_challenge_leaderboard(TestBase):

    def test_challenge_leader_board_status_get(self):
        self.create_invitation_from_user_to_user_2()
        self.client.login(password='password_2', username='username_2')
        response = self.client.get('/challenges/challenge_leaderboard/1/')
        self.assertEqual(response.status_code, 200)

    def test_invalid_challenge_leader_board_status_get(self):
        self.client.login(password='password_2', username='username_2')
        response = self.client.get('/challenges/challenge_leaderboard/1/')
        self.assertEqual(response.status_code, 404)