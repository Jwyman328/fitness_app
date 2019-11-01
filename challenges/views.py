import operator
import datetime

from django.shortcuts import render
from django.views.generic import CreateView, ListView, UpdateView, DetailView, TemplateView
from django.http.response import HttpResponse, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils.timezone import now

from .models import Challenge, Invitation_to_challenge, Invitation_status
from users.models import My_custom_user
from .forms import New_challenge_invitation_form

from django.forms.models import model_to_dict


# Create your views here.


class Create_a_challenge_view(LoginRequiredMixin, CreateView):
    """Allow user to create a challenge invitation object and challenge object.
    
    Send challenge invitation to invitees, submit current user to challenge created.

    """ 
    template_name = 'make_a_challenge.html'
    model = Invitation_to_challenge
    form_class = New_challenge_invitation_form
    success_url = '/challenges/Accepted_challenges_list'

    def get_form_kwargs(self): #https://gist.github.com/vero4karu/ec0f82bb3d302961503d
        """Pass user personal key to the related form"""
        kwargs = super(Create_a_challenge_view, self).get_form_kwargs()
        kwargs['user_id'] = self.request.user.pk
        return kwargs

    def create_invitor_status_accepted(self): 
        """Set the current user challenge invitation status to accepted."""
        this_user_model_id  = (self.request.user.id)
        invitor_user_model_obj = My_custom_user.objects.get(id=this_user_model_id)
        # get this invitation in updatable add form
        this_invitation = Invitation_to_challenge.objects.get(id=self.id)
        this_invitation.Invitation.add(invitor_user_model_obj)

    def form_valid(self, form):
        """Create invivation_status object for current user and set status to accepted.
        
        Actions take place after the form is submitted.
        """
        form.instance.invitor_user_model = self.request.user
        form.instance.username_of_invitor = self.request.user.username
        status_obj = Invitation_status.objects.create(invitee=self.request.user, status='accepted' )
        status_obj.save()
        # create a challenge, but only put the invitee as the only participant as of right now 
        return super().form_valid(form)


class Accept_deny_challenge_view(LoginRequiredMixin, ListView):
    """Mailbox for all challenge invitations that have not been accepted or rejected.
    
    """
    template_name = 'accept__deny_challenge.html'
    model = Invitation_to_challenge
    success_url = '/'

    # give the template just this users invitations that have not been accepted 
    def unanswered_challenge_invitations_returned(self):
        """Check for challenge invitations with status idle and return a list of them."""
        current_user_obj = self.request.user
        all_invitations_status_objects = current_user_obj.invitation_status_set.filter(status='idle')
        return all_invitations_status_objects


class Update_invitation_status(LoginRequiredMixin, UpdateView):
    """Allow the user to change their invitation status from idle to rejected or accpeted."""
    template_name = 'update_invitation_status.html'
    model = Invitation_status
    fields = ['status']
    success_url = '/challenges/pending_invitations'

    def form_valid(self, form):
        """ """
        
        def change_status():
            """Add user as a partipant if they have set invitation status to accepted."""
            current_status = form.instance.status  # get status submitted in the update form
            if current_status == 'accepted': # add them to the participants:
                challenges = form.instance.invitation.challenge_set.all() # get challenges related to this invitation
                for challenge in challenges:
                    challenge.participants.add(self.request.user) # add this user to to the participants of this challenge 

        change_status()
        return super().form_valid(form)

 
class Accepted_challenges_view(LoginRequiredMixin, ListView):
    """Show a list of all challenges accepted by the user."""
    template_name = 'Accepted_challenges_list.html'
    model = Invitation_to_challenge
    
    def accepted_challenge_invitations(self):
        """Return a list of accepted challenges.
        
        Before returning the list, if this user has created a challenged
        set that challenges invitation status object to the correct invitation pk.

        """

        def set_creator_of_invitation():
            """Add the invitation object to the invitation status database for the creator of the challenge
            
            When a challenge is created and an invitation is sent, the creator
            does not have the invitaion obj attached to the invitation status 
            object. To correct this the creator's invitation status object must 
            take the invitation object from the invitation status object one 
            in front of it (by pk), which will be one of the users invited
            who contains the correct invitation object pk. This invitation object
            will then be added as the creators status object invitation.

            """
            all_users_invitations_created = self.request.user.invitation_to_challenge_set.all() #get all invitations
            #get this users invitation_status that are null
            all_users_invitation_status_null = self.request.user.invitation_status_set.filter(invitation=None)
            for obj in all_users_invitation_status_null:
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
        all_invitations_status_objects = current_user_obj.invitation_status_set.filter(status='accepted')
        current_challenges = all_invitations_status_objects.filter(invitation__end_date__gte=now_date)
        current_challenges = current_challenges.filter(invitation__start_date__lte=now_date)
        current_challenges = current_challenges.order_by('invitation__end_date')
        #all_invitations = current_user_obj.invitation_to_challenge_set.all()
        return(current_challenges)

    def future_challenge_data(self):
        """Gather and return only challenges in the future from today.
        
        The today, is in reference to which ever day in which 
        the function is referened to.

        """
        current_user_obj = self.request.user
        all_invitations_status_objects = current_user_obj.invitation_status_set.filter(status='accepted')
        # now get the ones that the end date are older than today 
        now_date = now()
        future_challenges = all_invitations_status_objects.filter(invitation__start_date__gt=now_date)
        future_challenges = future_challenges.order_by('-invitation__end_date')
        return(future_challenges)
        
            
class Past_accepted_challenges(LoginRequiredMixin, ListView):
    """Show a list of past accepted challenges."""
    template_name = 'Past_accepted_challenges.html'
    model= Invitation_to_challenge

    def past_challenge_data(self):
        """Return a list of past accepted challenges.
        
        Order such list from newest to oldest.
         """
        current_user_obj = self.request.user
        all_invitations_status_objects = current_user_obj.invitation_status_set.filter(status='accepted')
        # now get the ones that the end date are older than today 
        now_date = now()
        past_challenges = all_invitations_status_objects.filter(invitation__end_date__lt=now_date)
        past_challenges = past_challenges.order_by('-invitation__end_date')
        return(past_challenges)

   
def returnAllUserChallenges(request):

    def AllUserChallenges():
        current_user_obj = request.user
        now_date = now()
        #all_invitations = current_user_obj.Invitation.all()  # without the set
        all_invitations_status_objects = current_user_obj.invitation_status_set.filter(status='accepted')
        current_challenges = all_invitations_status_objects
        current_challenges = current_challenges.order_by('invitation__end_date')
        #all_invitations = current_user_obj.invitation_to_challenge_set.all()
        #return(current_challenges[0].invitation_id)
        # get a list of all challenges 
        challenge_and_participants = []
        for challenge in current_challenges:   
            myChallenge = Challenge.objects.get(id=challenge.invitation_id) # eventually change to an array
            myChallengeParticipants = myChallenge.participants.all() # all participants of this challenge
            challenge_and_participants.append({'participants':myChallengeParticipants, 'challenge':myChallenge})
            #return(myChallengeParticipants,myChallenge)
        #print(challenge_and_participants)
        #return(challenge_and_participants)
        myChallenge = Challenge.objects.get(id=current_challenges[0].invitation_id) # eventually change to an array
        myChallengeParticipants = myChallenge.participants.all() # all participants of this challenge

        return(challenge_and_participants)

    def leader_board_data(list_of_dictionaries):
        """Create and return a dict of each partipant and their total points.
        
        Each challenge will contain participants and each participant(user obj)
        contains a method that will generate a point total for each challenge,
        such method will be called to generate the users total points for that 
        challenge.

        """
        finalReturnList = []
        for dictionary in list_of_dictionaries:
            username_total = {}
            usernames = []
            points = []
            related_challenge = dictionary['challenge']
            challengeInfo = {'startDate': related_challenge.start_date, "endDate": related_challenge.end_date,
                'title':related_challenge.title, "field": related_challenge.challenge_health_field}
            participants = dictionary['participants']
            challenge_obj = related_challenge
            for participant in participants:
                # points_for_challenge is a user object method for generating point totals
                participant_total = participant.points_for_challenge( 
                    challenge_obj.start_date, challenge_obj.end_date,
                    challenge_obj.challenge_health_field)
                usernames.append(participant.username)
                points.append(participant_total)
            DictionaryToAddtoFinalReturnList = {'id': related_challenge.id, 'data':{'userNames':usernames, 'points':points}, 'challenge_info': challengeInfo}
            finalReturnList.append(DictionaryToAddtoFinalReturnList)
    
        return(finalReturnList)
    participants_challenges = AllUserChallenges()
    jsonAbleData = leader_board_data(participants_challenges)
    # i have a list the contains dictionaries that contain the participants and challenge object for each 
    #list_of_jsonableDicts = [for item in participants_challenges, leader_board_data(participants_challenges['participants'],participants_challenges['challenge_obj'])
    
    return JsonResponse(jsonAbleData, safe=False) # safe is false in order to send a list of dictionaries


def returnJsonCurrentChallenge(request):
    # this is the user i want request.user.id 

    def currentUserChallenges():
        current_user_obj = request.user
        now_date = now()
        #all_invitations = current_user_obj.Invitation.all()  # without the set
        all_invitations_status_objects = current_user_obj.invitation_status_set.filter(status='accepted')
        current_challenges = all_invitations_status_objects.filter(invitation__end_date__gte=now_date)
        current_challenges = current_challenges.filter(invitation__start_date__lte=now_date)
        current_challenges = current_challenges.order_by('invitation__end_date')
        #all_invitations = current_user_obj.invitation_to_challenge_set.all()
        #return(current_challenges[0].invitation_id)
        # get a list of all challenges 
        challenge_and_participants = []
        
        if len(current_challenges) > 0:
            for challenge in current_challenges:   
                myChallenge = Challenge.objects.get(id=challenge.invitation_id) # eventually change to an array
                myChallengeParticipants = myChallenge.participants.all() # all participants of this challenge
                challenge_and_participants.append({'participants':myChallengeParticipants, 'challenge':myChallenge})

            
            myChallenge = Challenge.objects.get(id=current_challenges[0].invitation_id) # eventually change to an array
            myChallengeParticipants = myChallenge.participants.all() # all participants of this challenge

        return(challenge_and_participants)

    def leader_board_data(list_of_dictionaries):
        """Create and return a dict of each partipant and their total points.
        
        Each challenge will contain participants and each participant(user obj)
        contains a method that will generate a point total for each challenge,
        such method will be called to generate the users total points for that 
        challenge.

        """
        finalReturnList = []
        for dictionary in list_of_dictionaries:
            username_total = {}
            usernames = []
            points = []
            related_challenge = dictionary['challenge']
            challengeInfo = {'startDate': related_challenge.start_date, "endDate": related_challenge.end_date,
                'title':related_challenge.title, "field": related_challenge.challenge_health_field}
            participants = dictionary['participants']
            challenge_obj = related_challenge
            for participant in participants:
                # points_for_challenge is a user object method for generating point totals
                participant_total = participant.points_for_challenge( 
                    challenge_obj.start_date, challenge_obj.end_date,
                    challenge_obj.challenge_health_field)
                usernames.append(participant.username)
                points.append(participant_total)
            DictionaryToAddtoFinalReturnList = {'data':{'userNames':usernames, 'points':points}, 'challenge_info': challengeInfo}
            finalReturnList.append(DictionaryToAddtoFinalReturnList)
    
        return(finalReturnList)
    participants_challenges = currentUserChallenges()
    jsonAbleData = leader_board_data(participants_challenges)
    # i have a list the contains dictionaries that contain the participants and challenge object for each 
    #list_of_jsonableDicts = [for item in participants_challenges, leader_board_data(participants_challenges['participants'],participants_challenges['challenge_obj'])
    
    return JsonResponse(jsonAbleData, safe=False) # safe is false in order to send a list of dictionaries

class Challenge_leaderboard(LoginRequiredMixin, DetailView):
    """For each challenge show participants and thier scores in order most-least."""
    template_name = 'challenge_leaderboard.html'
    model = Challenge

    #get all the users for this challenge  with participants
    # then for the start - finish proclaimed, get the points of that catagory
    # a function that calculates the challenge_catagory total
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        data = self.get_context_data(object=self.object)
        if self.request.GET:
                return JsonResponse({'data': "data"})
        return self.render_to_response(data)

    def leader_board_data(self):
        """Create and return a dict of each partipant and their total points.
        
        Each challenge will contain participants and each participant(user obj)
        contains a method that will generate a point total for each challenge,
        such method will be called to generate the users total points for that 
        challenge.

        """
        challenge_obj = self.get_object() # each challenge object gets a Challenge_leaderboard class
        participants = challenge_obj.participants.all()
        username_total = {} #'username': total
        for participant in participants:
            # points_for_challenge is a user object method for generating point totals
            participant_total = participant.points_for_challenge( 
                challenge_obj.start_date, challenge_obj.end_date,
                challenge_obj.challenge_health_field)
            participant_username = participant.username
            username_total[participant_username] = participant_total
        # order the dictionary based off totals
        sorted_dict = sorted(username_total.items(), key=operator.itemgetter(1), reverse=True)
        #print(sorted_dict)
        return(sorted_dict)
    
    

class GeneralChallenges(LoginRequiredMixin, TemplateView):
    template_name = 'general_challenges.html'
        
            



    

