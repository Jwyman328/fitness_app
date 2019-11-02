from django.contrib.sessions.middleware import SessionMiddleware
from django.test import Client, RequestFactory

from .base import TestBase
from ..models import Challenge, Invitation_to_challenge, Invitation_status
from ..forms import New_challenge_invitation_form
from ..views import Create_a_challenge_view
from users.models import My_custom_user

import datetime


class Test_new_challenge_invitation_form(TestBase):

    def test_create_challenge_from_client_redirects(self):
        self.client.login(username='username', password='password')

        session = self.client.session
        session['somekey'] = 'test'
        session.save()
        
        response = self.client.post('/challenges/new_challenge', data={
            'title': 'test_challenge', 'start_date': '2019-03-28', 
            'end_date': '2019-03-30', 'challenge_health_field':'sleep_points', #
            'invitees': str(self.user_2.id) })

        self.assertRedirects(response,  '/challenges/Accepted_challenges_list')

    def test_create_challenge_from_client(self):
        #self.client = Client()
        self.client.login(username='username', password='password')

        session = self.client.session
        session['somekey'] = 'test'
        session.save()
        
        response = self.client.post('/challenges/new_challenge', data={
            'title': 'test_challenge', 'start_date': '2019-03-28', 
            'end_date': '2019-03-30', 'challenge_health_field':'sleep_points', #
            'invitees': str(self.user_2.id) })

        self.assertEqual(Challenge.objects.count(),1)

    def test_create_invitation_to_challenge_from_client(self):
        self.client = Client()
        self.client.login(username='username', password='password')

        session = self.client.session
        session['somekey'] = 'test'
        session.save()

        request = self.factory.post('/challenges/new_challenge',  data={
            'title': 'test_challenge', 'start_date': '2019-03-28', 
            'end_date': '2019-03-30', 'challenge_health_field':'sleep_points' #sleep_points
            ,'invitees': str(self.user_2.pk)
           })
        request.user = self.user
        request.user.username = self.user.username
        request.user.pk = 1
        request.user_id = 1 #self.user.id
        view = Create_a_challenge_view.as_view()
        response = Create_a_challenge_view.as_view()(request)
        #response = view(request)
        self.assertEqual(Invitation_to_challenge.objects.count(),1)
    
    def test_create_challenge_invitation_invitee_from_client(self):
        #self.client = Client()
        self.client.login(username='username', password='password')

        session = self.client.session
        session['somekey'] = 'test'
        session.save()
        
        response = self.client.post('/challenges/new_challenge', data={
            'title': 'test_challenge', 'start_date': '2019-03-28', 
            'end_date': '2019-03-30', 'challenge_health_field':'sleep_points', #
            'invitees': str(self.user_2.id) })

        # use the through db invitation_status to check who was invited
        invitation = Invitation_to_challenge.objects.get(id=1)
        invitation_to_user_2_exists =  Invitation_status.objects.get(id=self.user_2.id) 
        self.assertTrue(invitation_to_user_2_exists)

    def test_create_invitation_to_challenge(self):
        self.client.login(username='username', password='password')
        invitation = Invitation_to_challenge.objects.create( # need to put in a self.user_id
            title = 'test_challenge', start_date = datetime.date(2019,3,28),
            end_date= datetime.date(2019,3,30), challenge_health_field='Sleep',
             invitor_user_model=self.user,
            )
        # add an invitee
        invitation.invitees.add(self.user_2)
        first_invitation_invitees_db = Invitation_status.objects.get(id=1)
        # check invitation object created
        self.assertEqual(Invitation_to_challenge.objects.count(), 1)
    
      
    def test_invitation_to_challenge_object_creates_challenge_object(self):
        self.client.login(username='username', password='password')
        invitation = Invitation_to_challenge.objects.create( # need to put in a self.user_id
            title = 'test_challenge', start_date = datetime.date(2019,3,28),
            end_date= datetime.date(2019,3,30), challenge_health_field='Sleep',
             invitor_user_model=self.user,
            )
        # add an invitee
        invitation.invitees.add(self.user_2)
        first_invitation_invitees_db = Invitation_status.objects.get(id=1)
        # check challenge object created
        self.assertEqual(Challenge.objects.count(), 1) 

    def test_invitation_to_challenge_object_invitee(self):
        self.client.login(username='username', password='password')
        invitation = Invitation_to_challenge.objects.create( # need to put in a self.user_id
            title = 'test_challenge', start_date = datetime.date(2019,3,28),
            end_date= datetime.date(2019,3,30), challenge_health_field='Sleep',
             invitor_user_model=self.user,
            )
        # add an invitee
        invitation.invitees.add(self.user_2)
        first_invitation_invitees_db = Invitation_status.objects.get(id=1)
        #check invitation invitee db has the correct invitee
        self.assertEqual(first_invitation_invitees_db.invitee, self.user_2)

    def setup_view(self,view, request, *args, **kwargs):
        """Mimic as_view() returned callable, but returns view instance.

        args and kwargs are the same you would pass to ``reverse()``

        """
        view.request = request
        view.args = args
        view.kwargs = kwargs
        return view
    
    def test_try_factory(self):
        self.factory = RequestFactory()
        self.client.login(username='username', password='password')
        request = self.factory.post('/challenges/new_challenge',
            data={'title': 'test_challenge', 'start_date': '2019-03-28', 
            'end_date': '2019-03-30', 'challenge_health_field':'sleep_points', #sleep_points
            'invitees':str(self.user_2.id)})
        response = self.client.post('/challenges/new_challenge',
            data={'title': 'test_challenge', 'start_date': '2019-03-28', 
            'end_date': '2019-03-30', 'challenge_health_field':'sleep_points', #sleep_points
            'invitees':str(self.user_2.id)})
        request.user = self.user
        request.user.username = self.user.username
        view= Create_a_challenge_view()
        #view = self.setup_view(view, request,  user_id=1 )
        view = Create_a_challenge_view.as_view()
        #response = view(request)
        self.assertRedirects(response, '/challenges/Accepted_challenges_list')



        

        
        

    