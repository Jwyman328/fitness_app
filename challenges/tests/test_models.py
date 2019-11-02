
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import Client, RequestFactory

from .base import TestBase
from ..models import Challenge, Invitation_to_challenge, Invitation_status
from ..forms import New_challenge_invitation_form
from ..views import Create_a_challenge_view
from users.models import My_custom_user

import datetime
from unittest import skip


class Test_invitation_to_challenge(TestBase):
    
    def test_invitation_to_challenge_creation(self):
        self.create_invitation_to_challenge_from_model()
        # make sure an invitation to challenge object is created 
        #invitation = Invitation_to_challenge.objects.get(id=1)
        self.assertEqual(Invitation_to_challenge.objects.count(),1)

    def test_invitation_input_correct(self):
        self.create_invitation_to_challenge_from_model()
        invitation = Invitation_to_challenge.objects.get(id=1)

        self.assertEqual(invitation.challenge_health_field, 'water_points')
        self.assertEqual(invitation.invitor_user_model, self.user)
        self.assertEqual(invitation.username_of_invitor, self.user.username)
        self.assertEqual(invitation.challenge_health_field, 'water_points')
        self.assertEqual(invitation.start_date, datetime.date(2019,3,28) )
        self.assertEqual(invitation.end_date, datetime.date(2019,3,30) )


class Test_challenge(TestBase):

    def test_invitation_to_challenge_creation_creates_challenge(self):
        self.create_invitation_to_challenge_from_model()
        self.assertEqual(Challenge.objects.count(),1)
    
    def test_invitation_to_challenge_adds_invitor_to_participants(self):
        self.create_invitation_to_challenge_from_model()
        challenge = Challenge.objects.get(id=1)
        participants_query = challenge.participants.all()
        first_participant = participants_query.get(id=1)

        self.assertEqual(first_participant, self.user ) #self.user

    def test_challenges_input_correct(self):
        self.create_invitation_to_challenge_from_model()
        challenge = Challenge.objects.get(id=1)
        invitation = Invitation_to_challenge.objects.get(id=1)

        self.assertEqual(challenge.title, 'test_title')
        self.assertEqual(challenge.invitations, invitation)
        self.assertEqual(challenge.start_date,  datetime.date(2019,3,28))
        self.assertEqual(challenge.end_date,  datetime.date(2019,3,30))
        self.assertEqual(challenge.challenge_health_field, 'water_points')
        

class Test_Invitation_status(TestBase):

    def test_invitation_status_db_created_from_invitation_creation(self):
        """test one statuses exist user_2 """
        self.create_invitation_to_challenge_from_model()
        invitation = Invitation_to_challenge.objects.get(id=1)
        all_invitations_pending = invitation.invitees.all()

        self.assertEqual(all_invitations_pending.count(), 1)

