
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
        this_user_model_id  = str(self.invitor_user_model.id)
        invitor_user_model_obj = My_custom_user.objects.get(id='this_user_model_id')
        invitor_username = str(invitor_user_model_obj.username)
        return invitor_username

    def create_challenge(self):
        this_invitation = Invitation_to_challenge.objects.get(id = self.id)
        challenge_created = Challenge.objects.create(title=self.title, 
            invitations=this_invitation, start_date=self.start_date, 
            end_date=self.end_date, 
            challenge_health_field=self.challenge_health_field)
        return challenge_created

    def create_invitor_status_accepted(self): 
        this_user_model_id  = str(self.invitor_user_model.id)
        invitor_user_model_obj = My_custom_user.objects.get(id=this_user_model_id)
        # get this invitation in updatable add form
        this_invitation = Invitation_to_challenge.objects.get(id=self.id)
        this_invitation.Invitation.add(invitor_user_model_obj)

    def save(self, *args, **kwargs):
        
        is_new = True if not self.id else False # https://stackoverflow.com/questions/28264653/how-create-new-object-automatically-after-creating-other-object-in-django
        super(Invitation_to_challenge, self).save(*args, **kwargs)
        if is_new:
            # make the inivation
            challenge_created = self.create_challenge()
            # then add the participants 
            # have to use the custom through model Invitation_status
            challenge_created.participants.add(self.invitor_user_model)

            # add the invitor to the challenges_invitation_status

    def __str__(self):
        return self.title

class Invitation_status(models.Model):
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

    def set_status_accepted(self):
        # get this invitation_status_model 
        this_invitation_status_model_obj = Invitation_status.objects.filter(id=self.id)
        this_invitation_status_model_obj.update(status=accepted)


  