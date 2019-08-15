from django.shortcuts import render
from django.views.generic import CreateView, ListView, UpdateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Challenge, Invitation_to_challenge, Invitation_status
from users.models import My_custom_user
from .forms import New_challenge_invitation_form
import operator
from django.contrib import messages
from django.utils.timezone import now


# Create your views here.

class Create_a_challenge_view(LoginRequiredMixin, CreateView):

    template_name = 'make_a_challenge.html'
    model = Invitation_to_challenge
    form_class = New_challenge_invitation_form
    success_url = '/challenges/Accepted_challenges_list'

    def get_form_kwargs(self): #https://gist.github.com/vero4karu/ec0f82bb3d302961503d
        # pass variables from the view to the form
        kwargs = super(Create_a_challenge_view, self).get_form_kwargs()
        kwargs['user_id'] = self.request.user.pk
        return kwargs

    def create_invitor_status_accepted(self): # delete
        # have to do the add magic to this thing 
        this_user_model_id  = (self.request.user.id)
        invitor_user_model_obj = My_custom_user.objects.get(id = this_user_model_id)
        # get this invitation in updatable add form
        this_invitation = Invitation_to_challenge.objects.get(id = self.id)
        this_invitation.Invitation.add(invitor_user_model_obj)

    

    def form_valid(self, form):
        form.instance.invitor_user_model = self.request.user
        form.instance.username_of_invitor = self.request.user.username
        status_obj = Invitation_status.objects.create(invitee = self.request.user , status = 'accepted' )
        status_obj.save()
        
        # create a challenge, but only put the invitee as the only participant as of right now 
        return super().form_valid(form)


    def unanswered_challenge_invitations(self):

        current_user_obj = self.request.user
        all_invitations_status_objects = current_user_obj.invitation_status_set.filter(status = 'idle')
        if all_invitations_status_objects:
            messages.add_message(self.request, messages.INFO, 'Pending Invitation, to accept or reject go to Challenges -> Pending invitations')


class Accept_deny_challenge_view(LoginRequiredMixin, ListView):
    template_name = 'accept__deny_challenge.html'
    model = Invitation_to_challenge
    success_url = '/'

    # give the template just this users invitations that have not been accepted 
    def unanswered_challenge_invitations_returned(self):

        current_user_obj = self.request.user
        all_invitations_status_objects = current_user_obj.invitation_status_set.filter(status = 'idle')
        return all_invitations_status_objects

    def unanswered_challenge_invitations(self):

        current_user_obj = self.request.user
        all_invitations_status_objects = current_user_obj.invitation_status_set.filter(status = 'idle')
        if all_invitations_status_objects:
            messages.add_message(self.request, messages.INFO, 'Pending Invitation, to accept or reject go to Challenges -> Pending invitations')
        

class Update_invitation_status(LoginRequiredMixin, UpdateView):
    template_name = 'update_invitation_status.html'
    model = Invitation_status
    fields = ['status']

    success_url = '/challenges/pending_invitations'


    def form_valid(self, form):

        # get the object

        def change_status():
            current_status = form.instance.status 
            if current_status == 'accepted': # add them to the participants:
                # get the invitation_id
                # must add this user as participant in the challenge if they change thier status to accepted
                challenges = form.instance.invitation.challenge_set.all()
                for challenge in challenges:
                    challenge.participants.add(self.request.user)



        change_status()
        return super().form_valid(form)

    
    def unanswered_challenge_invitations(self):

        current_user_obj = self.request.user
        all_invitations_status_objects = current_user_obj.invitation_status_set.filter(status = 'idle')
        if all_invitations_status_objects:
            messages.add_message(self.request, messages.INFO, 'Pending Invitation, to accept or reject go to Challenges -> Pending invitations')

            
class Accepted_challenges_view(LoginRequiredMixin, ListView):
    template_name = 'Accepted_challenges_list.html'
    model = Invitation_to_challenge
    
    def accepted_challenge_invitations(self):
        # get all the invitations that relate to this user
        # get all the challenges that this user is in
        # then only get the invitations that are not related to the challenges he is in
        def set_creator_of_invitation():
            ''' when a user creates a challenge they are added to the invitation list
            but without an invitation object attached, this function corrects that'''
            all_users_invitations_created = self.request.user.invitation_to_challenge_set.all()
            #get this users invitation_status that are null
            all_users_invitation_status_null = self.request.user.invitation_status_set.filter(invitation = None)
            for obj in all_users_invitation_status_null:
                # get id 
                # add 1 to id
                # get that id obj invitation
                # then put the invitation in that original id
                obj_id = obj.id
                obj_id_plus_one = int(obj.id) + 1
                my_invitation_status_obj = Invitation_status.objects.get(id=obj_id_plus_one)
                my_invitation_obj = my_invitation_status_obj.invitation
                obj.invitation = my_invitation_obj
                obj.save()
        set_creator_of_invitation()
        # to access the status must go to the Invitation_status model 
        current_user_obj = self.request.user
        now_date = now()
        #all_invitations = current_user_obj.Invitation.all()  # without the set
        all_invitations_status_objects = current_user_obj.invitation_status_set.filter(status = 'accepted')
        current_challenges = all_invitations_status_objects.filter(invitation__end_date__gte = now_date)
        current_challenges = current_challenges.filter(invitation__start_date__lte = now_date)
        current_challenges = current_challenges.order_by('invitation__end_date')
        #all_invitations = current_user_obj.invitation_to_challenge_set.all()
       
        return(current_challenges)


    def future_challenge_data(self):
        current_user_obj = self.request.user
        all_invitations_status_objects = current_user_obj.invitation_status_set.filter(status = 'accepted')
        # now get the ones that the end date are older than today 
        now_date = now()
        future_challenges = all_invitations_status_objects.filter(invitation__start_date__gt = now_date)
        future_challenges = future_challenges.order_by('-invitation__end_date')
        return(future_challenges)

    def unanswered_challenge_invitations(self):

        current_user_obj = self.request.user
        all_invitations_status_objects = current_user_obj.invitation_status_set.filter(status = 'idle')
        if all_invitations_status_objects:
            messages.add_message(self.request, messages.INFO, 'Pending Invitation, to accept or reject go to Challenges -> Pending invitations')

            

class Past_accepted_challenges(LoginRequiredMixin, ListView):
    template_name = 'Past_accepted_challenges.html'
    model= Invitation_to_challenge


    def past_challenge_data(self):
        current_user_obj = self.request.user
        all_invitations_status_objects = current_user_obj.invitation_status_set.filter(status = 'accepted')
        # now get the ones that the end date are older than today 
        now_date = now()
        past_challenges = all_invitations_status_objects.filter(invitation__end_date__lt = now_date)
        past_challenges = past_challenges.order_by('-invitation__end_date')
        return(past_challenges)

    def unanswered_challenge_invitations(self):

        current_user_obj = self.request.user
        all_invitations_status_objects = current_user_obj.invitation_status_set.filter(status = 'idle')
        if all_invitations_status_objects:
            messages.add_message(self.request, messages.INFO, 'Pending Invitation, to accept or reject go to Challenges -> Pending invitations')

            

class Challenge_leaderboard(LoginRequiredMixin, DetailView):
    template_name = 'challenge_leaderboard.html'
    model = Challenge

    #get all the users for this challenge  with participants
    # then for the start - finish proclaimed, get the points of that catagory
    # a function that calculates the challenge_catagory total

    def leader_board_data(self):
        challenge_obj = self.get_object()
        participants = challenge_obj.participants.all()
        username_total = {} #'username': total
        for participant in participants:
            participant_total = participant.points_for_challenge(challenge_obj.start_date, challenge_obj.end_date, challenge_obj.challenge_health_field)
            participant_username = participant.username
            username_total[participant_username] = participant_total
        
        # order the dictionary based off total
        #username_total = sorted(username_total)
        sorted_dict = sorted(username_total.items(), key=operator.itemgetter(1), reverse=True)
        
        return(sorted_dict)

    
    def unanswered_challenge_invitations(self):

        current_user_obj = self.request.user
        all_invitations_status_objects = current_user_obj.invitation_status_set.filter(status = 'idle')
        if all_invitations_status_objects:
            messages.add_message(self.request, messages.INFO, 'Pending Invitation, to accept or reject go to Challenges -> Pending invitations')

            



    

