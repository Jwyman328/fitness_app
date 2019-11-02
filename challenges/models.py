
from django.db import models
from django.urls import reverse
from django.utils.timezone import now
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db.models import Sum

from users.models import My_custom_user
from users.models import My_custom_user


# Create your models here.

class Challenge(models.Model):
    """Allow users to compete against other users for a time period, over a specific health catagory.
    
    Args:
        challenge_health_field_choices(list of tuples): options for health catagories
        title(str): title of the challenge
        participants(M2M): database of users that have accepted the related challenge invitation
        invitations(FK object): related invitation object for each challenge
        start_Date(DateTime): Start date of the challenge
        end_date(DateTime): End date of the challenge 
        challenge_health_field(str): A single challenge health field that users compete for points over
  
    """
    challenge_health_field_choices = [
        ('sleep_points', 'Sleep'),('water_points', 'Water'), 
        ('clean_eating_points', 'Clean Eating'), ('step_points', 'Steps'),
        ('total_points', 'Total Points'),('workout_points', 'Workout')]

    title = models.CharField(max_length=100)
    participants = models.ManyToManyField(
        'users.My_custom_user', related_name='challenges', blank=True)
    invitations = models.ForeignKey(
        'Invitation_to_challenge', on_delete= models.CASCADE,
         null=True, blank=True)
    start_date = models.DateField(
        default=now, editable=True, help_text='year-month-day')
    end_date = models.DateField(
        default=now, editable=True, help_text='year-month-day')
    challenge_health_field = models.CharField(
        max_length=10000, choices=challenge_health_field_choices, default='total_points')

    def __str__(self):
        return self.title


class Invitation_to_challenge(models.Model):
    """Invitation to a challenge send to users to be accepted or rejected.
    
    Args:
        challenge_health_field_choices(list of tuples): options for health catagories
        start_Date(DateTime): Start date of the challenge
        end_date(DateTime): End date of the challenge 
        invitees(M2M): database of users that have been sent an invitation
        invitor_user_model(FK obj): User obj who has created and sent out the invitation
        user_name_of_invitor(str): Username of the invitor
        title(str): title of the invitation/challenge

    """

    challenge_health_field_choices = [
        ('sleep_points', 'Sleep'), ('water_points', 'Water'), 
        ('clean_eating_points' ,'Clean Eating'), ('step_points', 'Steps'),
        ('total_points', 'Total Points'),('workout_points', 'Workout')]

    start_date = models.DateField(
        default=now, editable=True, help_text='year-month-day')
    end_date = models.DateField(
        default=now, editable=True, help_text='year-month-day')
    challenge_health_field = models.CharField(
        max_length=10000, choices=challenge_health_field_choices,
        default='total_points')
    invitees = models.ManyToManyField(
        'users.My_custom_user', through='Invitation_status',
        related_name='Invitation',
        help_text='invite as many people to the challenge!')
    invitor_user_model = models.ForeignKey(
        'users.My_custom_user', on_delete=models.CASCADE,
         null=True, blank=True) # set this automatically 
    username_of_invitor = models.CharField(
        max_length=100, null=True, blank=True)
    title=models.CharField(max_length=200)
    
    def invitor_username(self):
        """Get and return Invitation to challenges creator's username.
        
        Args:
            this_user_model_id(str): id of the user model
            invitor_user_model_obj(obj): user model object of the invitation invitor
            invitor_username(str): username of the invitor

        """
        this_user_model_id  = str(self.invitor_user_model.id)
        invitor_user_model_obj = My_custom_user.objects.get(id='this_user_model_id')
        invitor_username = str(invitor_user_model_obj.username)
        return invitor_username

    def create_challenge(self):
        """Create and return a challenge object from the invitation arguments.
        
        Args:
            this_invitation(obj): invitation object 
            challenge_created(obj): newly created challenge object

        """
        this_invitation = Invitation_to_challenge.objects.get(id = self.id)
        challenge_created = Challenge.objects.create(title=self.title, 
            invitations=this_invitation, start_date=self.start_date, 
            end_date=self.end_date, 
            challenge_health_field=self.challenge_health_field)
        return challenge_created

    def create_invitor_status_accepted(self):  # believe i can delete this func
        """ Add the creator of the invitation as someone who recieved an invitation.
        
        Args:
            this_user_model_id(str): id of the invitor's user object
            invitor_user_model_obj(obj): invitor's user object
            this_invitation(obj): current invitation object
            
         """
        this_user_model_id  = str(self.invitor_user_model.id)
        invitor_user_model_obj = My_custom_user.objects.get(id=this_user_model_id)
        # get this invitation in updatable add form
        this_invitation = Invitation_to_challenge.objects.get(id=self.id)
        this_invitation.Invitation.add(invitor_user_model_obj) 

    def convert_field_name_to_readable_field_name(self):
        """return a more readable version of the health_field"""
        
        return(dict(self.challenge_health_field_choices).get(self.challenge_health_field))

    def save(self, *args, **kwargs):
        """ save the invitation object,after create a corresponding challenge obj.

        As well add the creator of the invitation as a participant of the challenge.
        
        Args:
            challenge_created(obj): challenge object that corresponds to this invitation object
            
        """
        is_new = True if not self.id else False # https://stackoverflow.com/questions/28264653/how-create-new-object-automatically-after-creating-other-object-in-django
        super(Invitation_to_challenge, self).save(*args, **kwargs)
        if is_new:
            # after invitation is made
            challenge_created = self.create_challenge()
            # then add the participants 
            # have to use the custom through model Invitation_status
            challenge_created.participants.add(self.invitor_user_model)

            # add the invitor to the challenges_invitation_status

    def __str__(self):
        return self.title

class Invitation_status(models.Model):
    """Through model for each invitation that contains the status of each invitation.
    
    Args:
        idle(str): status that the invitation to the challenge has not been accepted or rejected
        accepted(str): status that the invitation to the challenge has been accepted
        rejected(str): status that the invitation to the challenge has been rejected
        status_options(lst):: list of choices for the invitation status
        invitation(obj): Invitation object
        invitee(obj): User object that has been invited to the challenge, and recieved an invitation
        status(str): Status of the invitation to the challenge, accepted, rejected, or idle

    """
    # the throughh model for Invitation_to_challenge_invitees 
    # this way for each invitation to every user, we can see if they accept, deny or its idle 

    idle = 'idle'
    accepted = 'accepted'
    rejected = 'rejected'
    status_options = [(idle, 'idle'), (accepted, 'accepted'), (rejected, 'rejected')]
    invitation = models.ForeignKey(
        'Invitation_to_challenge', on_delete=models.SET_NULL,
        null=True, blank=True)
    invitee = models.ForeignKey(
        'users.My_custom_user', on_delete=models.SET_NULL,
        null=True, blank=True)
    status = models.CharField(
        max_length=100, choices=status_options, default=idle  )

    def set_status_accepted(self): # beleive it is not used, can delete
        """Set this objects status to accepted.
    
        Args:
            this_invitation_status_model_obj(obj): this invitation_status object in updateable form
        
        """
        this_invitation_status_model_obj = Invitation_status.objects.filter(id=self.id)
        this_invitation_status_model_obj.update(status=accepted)


  