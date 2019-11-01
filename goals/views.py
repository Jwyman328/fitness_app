import datetime, time

from django.shortcuts import render
from django.http.response import HttpResponse, JsonResponse
from django.urls import reverse
from django.views.generic import TemplateView, CreateView, ListView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.contrib import messages
from django.utils.timezone import now

from app.models import User_point_input_model
from app.models import Point_model, Point_goals
from app.forms import Point_goals_form, Health_input_form
from users.models import My_custom_user

from django.forms.models import model_to_dict

# Create your views here.


class Set_goals_view(LoginRequiredMixin, CreateView):
    """Create a goal object."""
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
    
    

     
class See_goals_view(LoginRequiredMixin, ListView):
    """Show all current and future goals."""
    model = Point_goals
    template_name = 'see_goal_list.html'

    #send the goals based off of year and month 
    def goals(self):
        """Return current users current goals.
        
        Args:
            now_date(DateTime): today's current date
            current_user_goals: a queryset of all the currents user's goals
            date_ordered_goals(querset): users goals with an end date greater or equal to today
                and a start date less than or equal to today

        """
        # order the goals by the current user
        # order the goals by there date 
        # have a table with point goal, start date, end date, is active check mark, accomplished goal or not 
        now_date = now()
        current_user_goals = Point_goals.objects.filter(user=self.request.user)
        date_ordered_goals = current_user_goals.order_by('goal_end_date')
        date_ordered_goals = date_ordered_goals.filter(goal_end_date__gte=now_date)
        date_ordered_goals = date_ordered_goals.filter(goal_start_date__lte=now_date)
        return date_ordered_goals

    def future_goals(self):
        """ Return all user goals that start later than today.
        
        Args:
            current_user_goals(QuerySet): current users goals
            now_date(DateTime): Today's date
            past_goals(QuerySet): User's goals that start before today

        """
        current_user_goals = Point_goals.objects.filter(user=self.request.user)
        now_date = now()
        past_goals = current_user_goals.filter(goal_start_date__gt=now_date)
        past_goals = past_goals.order_by('-goal_end_date')
        return(past_goals)


class Past_goals(LoginRequiredMixin, ListView):
    """Show all past user goals. """
    model = Point_goals
    template_name = 'past_goal_list.html'
    
    def past_goals(self):
        """
        
        Args:
            current_user_goals(QuerySet): current users goals
            now_date(DateTime): Today's date
            past_goals(QuerySet): User's goals that end before today

        """
        current_user_goals = Point_goals.objects.filter(user=self.request.user)
        now_date = now()
        past_goals = current_user_goals.filter(goal_end_date__lt=now_date)
        past_goals = past_goals.order_by('-goal_end_date')
        return(past_goals)


class Delete_goal(LoginRequiredMixin, DeleteView):
    """Allow user to delete a goal. """
    template_name = 'delete_goal.html'
    model = Point_goals
    success_url = '/goals/see_goals'

    def get_context_data(self, **kwargs): # might not need this 
        """Send all user goals, ordered by date to the corresponding template page."""
        context = super(Delete_goal, self).get_context_data(**kwargs)
        user_goals = Point_goals.objects.filter(user=self.request.user)
        user_goals = Point_goals.objects.order_by('date') 
        # so they are in the same order as the see_goal_list page represents them 

        context.update({'user_goals' : user_goals})
        return context

class specific_goal_graph(LoginRequiredMixin, DetailView):
    """ return page that will include graph of each goal """
    template_name = 'specific_goal_graph.html' 
    #model = Point_model
    queryset = Point_goals.objects.all()

    def points(self):
        """return a queryset of every point_object """
        return Point_model.objects.all()
    
    def goals(self):
        """ Return all of the users goals."""
        point_goal_ls =  Point_goals.objects.filter(user=self.request.user)
        return point_goal_ls

class GeneralGoals(LoginRequiredMixin, TemplateView):
    template_name = 'general_goals.html'


def returnAllGoalsDataJson(request):
        """return all user goal models in json form """
        userPointModels = Point_goals.objects.filter(user=request.user)
        list_of_jsonableDicts = []
        for pointData in userPointModels:
            pointModel_data_jsonable = model_to_dict(pointData)
            list_of_jsonableDicts.append(pointModel_data_jsonable)
        
        sorted_date = sorted(list_of_jsonableDicts, key=lambda x: x["goal_end_date"])
        
        return JsonResponse(sorted_date, safe=False)

def returnCurrentGoals(request):
        "return goals for user that are currently active, in json format"
        current_user_obj = request.user
        now_date = now()
        #all_invitations = current_user_obj.Invitation.all()  # without the set
        all__user_point_goal_objects = Point_goals.objects.filter(user=request.user)
        current_goals = all__user_point_goal_objects.filter(goal_end_date__gte=now_date)
        current_goals = current_goals.filter(goal_start_date__lte=now_date)
        current_goals = current_goals.order_by('goal_end_date')
        #all_invitations = current_user_obj.invitation_to_challenge_set.all()
        #return(current_challenges[0].invitation_id)
        # get a list of all challenges 
        list_of_jsonableDicts = []
        for pointData in current_goals:
            pointModel_data_jsonable = model_to_dict(pointData)
            list_of_jsonableDicts.append(pointModel_data_jsonable)
        
        sorted_date = sorted(list_of_jsonableDicts, key=lambda x: x["goal_end_date"])
        
        return JsonResponse(sorted_date, safe=False)