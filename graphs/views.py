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


# Create your views here.
class Daily_point_recap_view(LoginRequiredMixin, DetailView):
    template_name = 'daily_point_graph.html'
    #model = Point_model
    queryset = Point_model.objects.all()

    def points(self):
        return Point_model.objects.all()
    
    def goals(self):
        """ make only the current users goals accesible to him"""
        point_goal_ls =  Point_goals.objects.filter(user = self.request.user)

        return point_goal_ls

    def unanswered_challenge_invitations(self):

        current_user_obj = self.request.user
        #all_invitations = current_user_obj.Invitation.all()  # without the set
        all_invitations_status_objects = current_user_obj.invitation_status_set.filter(status = 'idle')
        #all_invitations = current_user_obj.invitation_to_challenge_set.all()
        if all_invitations_status_objects:
            messages.add_message(self.request, messages.INFO, 'Pending Invitation, to accept or reject go to Challenges -> Pending invitations')


class User_all_time_progress_graph_view(LoginRequiredMixin, ListView):
    template_name = 'User_all_time_progress_graph.html'
    model = Point_model

    def user_daily_points(self):        
        a_model_query_set = Point_model.objects.filter(user_id = self.request.user)
        a_model_query_set_date_ordered = a_model_query_set.order_by('date')

        all_daily_points = []
        for model_obj in a_model_query_set_date_ordered:
        
            model_obj_points_up_to_date = model_obj.total_points
            all_daily_points.append(model_obj_points_up_to_date)
        return all_daily_points
        
        
    def date_data(self):

        a_model_query_set = Point_model.objects.filter(user_id = self.request.user)
        a_model_query_set_date_ordered = a_model_query_set.order_by('date')

        all_dates = []
        
        
        for model_obj in a_model_query_set_date_ordered:
                
            
                model_obj_date = model_obj.date
                all_dates.append(model_obj_date)

                
                #model_obj_points_up_to_date = model_obj.up_to_date_total_points_accumulated
        return all_dates

    def points_up_to_date_data(self):

        a_model_query_set = Point_model.objects.filter(user_id = self.request.user)
        a_model_query_set_date_ordered = a_model_query_set.order_by('date')

        all_points_up_to_here = []
        for model_obj in a_model_query_set_date_ordered:
        
            model_obj_points_up_to_date = model_obj.up_to_date_total_points_accumulated
            all_points_up_to_here.append(model_obj_points_up_to_date)
        
        return all_points_up_to_here

    def unanswered_challenge_invitations(self):

        current_user_obj = self.request.user
        #all_invitations = current_user_obj.Invitation.all()  # without the set
        all_invitations_status_objects = current_user_obj.invitation_status_set.filter(status = 'idle')
        #all_invitations = current_user_obj.invitation_to_challenge_set.all()
        if all_invitations_status_objects:
            messages.add_message(self.request, messages.INFO, 'Pending Invitation, to accept or reject go to Challenges -> Pending invitations')



class Daily_points_graph_view(LoginRequiredMixin, ListView):
    template_name = "daily_points_graph.html"

    model = Point_model

    def user_daily_points(self):        
        a_model_query_set = Point_model.objects.filter(user_id = self.request.user)
        a_model_query_set_date_ordered = a_model_query_set.order_by('date')

        all_daily_points = []
        for model_obj in a_model_query_set_date_ordered:
        
            model_obj_points_up_to_date = model_obj.total_points
            all_daily_points.append(model_obj_points_up_to_date)
        return all_daily_points
        
        
    def date_data(self):

        a_model_query_set = Point_model.objects.filter(user_id = self.request.user)
        a_model_query_set_date_ordered = a_model_query_set.order_by('date')
        all_dates = []

        for model_obj in a_model_query_set_date_ordered:
                model_obj_date = model_obj.date
                all_dates.append(model_obj_date)
                #model_obj_points_up_to_date = model_obj.up_to_date_total_points_accumulated
        return all_dates

    def unanswered_challenge_invitations(self):

        current_user_obj = self.request.user
        #all_invitations = current_user_obj.Invitation.all()  # without the set
        all_invitations_status_objects = current_user_obj.invitation_status_set.filter(status = 'idle')
        #all_invitations = current_user_obj.invitation_to_challenge_set.all()
        if all_invitations_status_objects:
            messages.add_message(self.request, messages.INFO, 'Pending Invitation, to accept or reject go to Challenges -> Pending invitations')





  