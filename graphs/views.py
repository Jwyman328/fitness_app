import datetime, time

from django.shortcuts import render
from django.http.response import HttpResponse
from django.urls import reverse
from django.views.generic import TemplateView, CreateView, ListView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.contrib import messages

from app.models import User_point_input_model
from app.models import Point_model, Point_goals
from app.forms import Point_goals_form, Health_input_form
from users.models import My_custom_user


# Create your views here.
class Daily_point_recap_view(LoginRequiredMixin, DetailView):
    """Graph showing points for each health category fpr each day input."""
    template_name = 'daily_point_graph_json.html' 
    #model = Point_model
    queryset = Point_model.objects.all()

    def points(self):
        """return a queryset of every point_object """
        return Point_model.objects.all()
    
    def goals(self):
        """ Return all of the users goals."""
        point_goal_ls =  Point_goals.objects.filter(user=self.request.user)
        return point_goal_ls


class GeneralResults(LoginRequiredMixin, TemplateView):
    template_name = 'general_results.html'





  