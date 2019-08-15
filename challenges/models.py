
from django.db import models
from users.models import My_custom_user
from django.urls import reverse
from django.utils.timezone import now
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings
#from django_auto_one_to_one import AutoOneToOneModel
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from users.models import My_custom_user
from django.db.models import Sum

# Create your models here.

class Challenge(models.Model): # make uppercase 
    challenge_health_field_choices = [('sleep_points', 'Sleep'), ('water_points', 'Water'), ('clean_eating_points' , 
    'Clean Eating'), ('step_points', 'Steps'), ('total_points', 'Total Points'),('workout_points', 'Workout')]

    title = models.CharField(max_length = 100)
    participants = models.ManyToManyField('users.My_custom_user', related_name = 'challenges', blank = True)
    invitations = models.ForeignKey('Invitation_to_challenge', on_delete= models.CASCADE, null = True, blank = True)
    start_date = models.DateField(default= now, editable=True, help_text = 'year-month-day')
    end_date = models.DateField(default= now, editable=True, help_text = 'year-month-day')
    challenge_health_field = models.CharField(max_length = 10000, choices = challenge_health_field_choices, default = 'total_points')

    def __str__(self):
        return self.title

class Invitation_to_challenge(models.Model):
    challenge_health_field_choices = [('sleep_points', 'Sleep'), ('Water_points', 'Water'), ('clean_eating_points' , 
    'Clean Eating'), ('steps', 'Steps'), ('total_points', 'Total Points'),('workout_points', 'Workout')]

    start_date = models.DateField(default= now, editable=True, help_text = 'year-month-day')
    end_date = models.DateField(default= now, editable=True, help_text = 'year-month-day')
    challenge_health_field = models.CharField(max_length = 10000, choices = challenge_health_field_choices, default = 'total_points')
    invitees = models.ManyToManyField('users.My_custom_user', through = 'Invitation_status', related_name = 'Invitation', help_text = 'invite as many people to the challenge!')
    invitor_user_model = models.ForeignKey('users.My_custom_user', on_delete = models.CASCADE, null = True, blank = True) # set this automatically 
    username_of_invitor = models.CharField(max_length = 100, null = True, blank = True)
    title = models.CharField(max_length = 200)
    #status = models.CharField(max_length = 100, default = 'idle')
    
    def invitor_username(self):
        this_user_model_id  = str(self.invitor_user_model.id)
        invitor_user_model_obj = My_custom_user.objects.get(id = 'this_user_model_id')
        print(invitor_user_model_obj)
        invitor_username = str(invitor_user_model_obj.username)
        return invitor_username


    def create_challenge(self):
        this_invitation = Invitation_to_challenge.objects.get(id = self.id)
        challenge_created = Challenge.objects.create(title = self.title, 
        invitations = this_invitation, start_date = self.start_date, end_date = self.end_date,
        challenge_health_field = self.challenge_health_field)

        return challenge_created

    def create_invitor_status_accepted(self): # delete
        # have to do the add magic to this thing 
        this_user_model_id  = str(self.invitor_user_model.id)
        invitor_user_model_obj = My_custom_user.objects.get(id = this_user_model_id)
        # get this invitation in updatable add form
        this_invitation = Invitation_to_challenge.objects.get(id = self.id)
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

            #invitor_invitation_status_set.invitee.add(self.invitor_user_model)
            #set this user as a many to many 

    def __str__(self):
        return self.title

class Invitation_status(models.Model):
    # the throughh model for Invitation_to_challenge_invitees 
    # this way for each invitation to every user, we can see if they accept, deny or its idle 

    idle = 'idle'
    accepted = 'accepted'
    rejected = 'rejected'
    status_options = [(idle, 'idle'), (accepted, 'accepted'), (rejected, 'rejected') ]
    invitation = models.ForeignKey('Invitation_to_challenge', on_delete = models.SET_NULL, null = True, blank = True)
    invitee = models.ForeignKey('users.My_custom_user', on_delete = models.SET_NULL, null = True, blank = True)
    status = models.CharField(max_length = 100, choices = status_options, default = idle  )

    def set_status_accepted(self):
        # get this invitation_status_model 
        this_invitation_status_model_obj = Invitation_status.objects.filter(id = self.id)
        this_invitation_status_model_obj.update(status = accepted)

    # if invitation status is accepted, must add them to challenge participants


#class User_challenge_points(models.Model):


    # notes https://www.revsys.com/tidbits/tips-using-djangos-manytomanyfield/
    # you have to create the challenge before you can add participants 
    # to add participants you must use "add"
    # challenge_obj.participants. add(user_obj)

    # how to refer to a many to many group use set 
    # to see what challenges that each user  is involved in 
    # the_user.challenge_set.all()     # and this will show all the challenges the user has 
    
    # can not user set and user a more reader friendly output like 
    # the_user.challenges.all()  # so now we now this will return the users from this challenge 
    # to do this make a related_name field inside the participants field 
    #  participants = models.ManyToManyField('My_custom_user', related_name = 'users')

    # make a custom through model ?
    # i say first try it without and just use functions to display data 


## get related objects fields https://django-book.readthedocs.io/en/latest/chapter10.html
## you can get the object
## you just need to get the foriengn key field
## first get the object containing the foriegn key field
##* obj_with_forky = model.objects.get(id = 5) # choose any key, just a get a specific obj
## then get the foriegn key field 
##* foriegn_key_obj = obj_with_forky.ForiengnKeyField
## now you have access to all of that foriegn key objects fields

# you can do the reverse, get the original obj from inside the foreinkey_object
## foriegnKey_obj.original_model_set.all() or .filter() or .get 
## this will send you back a list of objects that that foriegn key has
### so parent_obj.childModelLowerCase_set.all() # will return me all the children objects


# accessing many to many 
## regular_obj.many2ManyModel.all() # this will get all the many2ManyModel objects
## specific_book.authors.all()  # so get all the many authers that this book has 

# now get all the specific books from an author 
## specific_author_object.bookModel_set.all() # this will return all this authors book objects
