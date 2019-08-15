from django.shortcuts import render
from django.http.response import HttpResponse
from django.urls import reverse
from django.views.generic import TemplateView, CreateView, ListView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from app.models import User_point_input_model
from app.models import Point_model , Point_goals
from app.forms import Point_goals_form, Health_input_form
from users.models import My_custom_user
import datetime, time
from django.db.models import Sum
from django.contrib import messages
from django.utils.timezone import now




# Create your views here.


class Set_goals_view(LoginRequiredMixin, CreateView):
    template_name = 'set_goals.html'
    model = Point_goals
    form_class = Point_goals_form
    success_url = '/goals/see_goals'

    def get_form_kwargs(self):
        kwargs = super(Set_goals_view, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs


    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def unanswered_challenge_invitations(self):

        current_user_obj = self.request.user
        all_invitations_status_objects = current_user_obj.invitation_status_set.filter(status = 'idle')
        if all_invitations_status_objects:
            messages.add_message(self.request, messages.INFO, 'Pending Invitation, to accept or reject go to Challenges -> Pending invitations')

     

class See_goals_view(LoginRequiredMixin, ListView):
    model = Point_goals
    template_name = 'see_goal_list.html'

    #send the goals based off of year and month 
    def goals(self):
        # order the goals by the current user
        # order the goals by there date 
        # have a table with point goal, start date, end date, is active check mark, accomplished goal or not 
        now_date = now()
        current_user_goals = Point_goals.objects.filter(user = self.request.user)
        date_ordered_goals = current_user_goals.order_by('goal_end_date')
        date_ordered_goals = date_ordered_goals.filter(goal_end_date__gte = now_date)
        date_ordered_goals = date_ordered_goals.filter(goal_start_date__lte = now_date)

        return date_ordered_goals

    def future_goals(self):
        
        current_user_goals = Point_goals.objects.filter(user = self.request.user)
        now_date = now()
        past_goals = current_user_goals.filter(goal_start_date__gt = now_date)
        past_goals = past_goals.order_by('-goal_end_date')

        return(past_goals)




    def unanswered_challenge_invitations(self):

        current_user_obj = self.request.user
        all_invitations_status_objects = current_user_obj.invitation_status_set.filter(status = 'idle')
        if all_invitations_status_objects:
            messages.add_message(self.request, messages.INFO, 'Pending Invitation, to accept or reject go to Challenges -> Pending invitations')

class Past_goals(LoginRequiredMixin, ListView):
    model = Point_goals
    template_name = 'past_goal_list.html'
    
    def past_goals(self):
        current_user_goals = Point_goals.objects.filter(user = self.request.user)
        now_date = now()
        past_goals = current_user_goals.filter(goal_end_date__lt = now_date)
        past_goals = past_goals.order_by('-goal_end_date')

        return(past_goals)


    def unanswered_challenge_invitations(self):

        current_user_obj = self.request.user
        all_invitations_status_objects = current_user_obj.invitation_status_set.filter(status = 'idle')
        if all_invitations_status_objects:
            messages.add_message(self.request, messages.INFO, 'Pending Invitation, to accept or reject go to Challenges -> Pending invitations')



class Delete_goal(LoginRequiredMixin, DeleteView):
    template_name = 'delete_goal.html'
    model = Point_goals
    success_url = '/goals/see_goals'

    def get_context_data(self, **kwargs): # might not need this 
        context = super(Delete_goal, self).get_context_data(**kwargs)
        user_goals = Point_goals.objects.filter(user = self.request.user)
        user_goals = Point_goals.objects.order_by('date') # so they are in the same order as the see_goal_list page represents them 

        context.update({'user_goals' : user_goals})
        return context
    def unanswered_challenge_invitations(self):

        current_user_obj = self.request.user
        all_invitations_status_objects = current_user_obj.invitation_status_set.filter(status = 'idle')
        if all_invitations_status_objects:
            messages.add_message(self.request, messages.INFO, 'Pending Invitation, to accept or reject go to Challenges -> Pending invitations')


    