import datetime, time

from django.shortcuts import render
from django.http.response import HttpResponse
from django.urls import reverse
from django.views.generic import TemplateView, CreateView, ListView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.contrib import messages

from .models import User_point_input_model
from .models import Point_model, Point_goals
from .forms import Point_goals_form, Health_input_form
from users.models import My_custom_user

# Create your views here.


class Homepage_view(LoginRequiredMixin, ListView):
    """A Simple homepage."""
     # make the datavisualizationpage a Detail view and generate a page for every point object
    template_name = 'home.html'
    queryset = User_point_input_model.objects.all()

    # check if there are any pending messages 
    def unanswered_challenge_invitations(self):
        """Check for challenge invitations, if found, create and send a message."""

        current_user_obj = self.request.user
        all_invitations_status_objects = (
            current_user_obj.invitation_status_set.filter(status = 'idle'))
        if all_invitations_status_objects:
            messages.add_message(self.request, messages.INFO,
                                """Pending Invitation, to accept or reject go
                                 to Challenges -> Pending invitations""")
        
            
class Daily_points_date_list(LoginRequiredMixin, ListView):
    """List of users health data points."""
    template_name = 'daily_points_date_list.html'
    model = Point_model

    def order_date_data(self):
        """Order and return point data by date, newest to oldest."""
        ordered_user_data = Point_model.objects.filter(user=self.request.user)
        order_date_data = ordered_user_data.order_by('-date')
        return order_date_data

    def unanswered_challenge_invitations(self):
        """Check for challenge invitations,if found, create and send a message"""
        current_user_obj = self.request.user
        all_invitations_status_objects = current_user_obj.invitation_status_set.filter(status='idle')
        if all_invitations_status_objects:
            messages.add_message(self.request, messages.INFO,
                                """Pending Invitation, to accept or 
                                reject go to Challenges -> Pending invitations""")

            
class Health_data_input(LoginRequiredMixin, CreateView):
    """A form allowing the user to create a Health data and corresponding point object."""
    template_name = 'health_data_input_form.html'
    model = User_point_input_model
    form_class = Health_input_form
    
    def get_form_kwargs(self):
        """Get and return the current user object to the Health input form."""

        kwargs = super(Health_data_input, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        """Input the current user object as the user in the health input form."""

        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        """Get the newly created health input objects pk, and return user to corresponging graph.
        
        if health model pk and point model pk differ, the incorrect pk will be given
        and the user will be returned to the wrong graph page,
        not representing the new health input object.
        """

        pk_value = int(self.object.pk) # get newly created health model obj pk
        return reverse('daily_point_graph', kwargs={'pk' : pk_value}) 

    def unanswered_challenge_invitations(self):
        """Check for challenge invitations,if found, create and send a message"""
        current_user_obj = self.request.user
        all_invitations_status_objects = current_user_obj.invitation_status_set.filter(status='idle')
        if all_invitations_status_objects:
            messages.add_message(self.request, messages.INFO,
                                """Pending Invitation, to accept or 
                                 reject go to Challenges -> Pending invitations""")

            
class Update_health_data_input(LoginRequiredMixin, UpdateView):
    """A update form allowing the user to change any Health data input, one at a time.
    
    As well, the corresponding point and goal objects will be updated as well.

    """
    template_name = 'update_daily_data_input.html'
    model = User_point_input_model
    fields = ['date', 'Hours_of_sleep','Water_100oz', 'clean_eating', 
              'workout_intensity', 'workout_amount_of_time', 'steps']
    
    def form_valid(self, form):

        def update_points():
            """ Update this health input object's corresponding point object
            
            recalculate all of the this update forms input in point form,
            and then input it into the corresponding point object.
            Update the total points acumulated for each user object

             """

            def water_clean_eating_point_func(water_or_clean_eating_true_false):
                """ if the input is true, return 10
                
                Args: 
                water_or_clean_eating_true_false (boolean): True false, if the user 
                ate clean or drank 100oz of water.

                return: int:10 if param true

                """
                if water_or_clean_eating_true_false == 1:
                    return 10.0
                else:
                    return 0.0 
            
            def point_goal_for_this_date():
                """ Return the point goal that applies to this health input object's date. """
                point_goal = 0
                all_point_goals = Point_goals.objects.filter(user=self.request.user) #current users point objects
                for obj in all_point_goals: 
                    if form.instance.date >= obj.goal_start_date and form.instance.date <= obj.goal_end_date: 
                        
                        point_goal = int(obj.point_goal)
                        #return int(point_goal)
                    else:
                        pass
                
                return point_goal
               
            sleep_points = form.instance.Hours_of_sleep * 3.3
            date = form.instance.date
            user = self.request.user
            workout_points = form.instance.workout_intensity * (form.instance.workout_amount_of_time * .2)
            clean_eating_points = water_clean_eating_point_func(form.instance.clean_eating)
            water_points = water_clean_eating_point_func(form.instance.Water_100oz)
            step_points = form.instance.steps * .001
            total_points = water_points + workout_points + sleep_points + clean_eating_points + step_points
            point_goal = point_goal_for_this_date()
            

            def update_user_sum_total_points():
                """ Update user's total points inside the user obj. """
                # before th model is update i need to acess the older data 
                current_user_updateable_version = My_custom_user.objects.filter(id=self.request.user.id) # filter for the current user in updateable query format
                current_user = My_custom_user.objects.get(id=self.request.user.id) 
                current_model_in_point_version = Point_model.objects.get(id=self.object.id)
                
                current_point_sum = current_user.total_points # former total points for the user
                former_input_of_total_points_for_this_date = current_model_in_point_version.total_points # incorrect this got the new points amount
                difference_in_old_and_new_points_for_this_input = total_points - former_input_of_total_points_for_this_date
                new_total_user_points_all_time_sum =  current_point_sum + difference_in_old_and_new_points_for_this_input 
                
                current_user_updateable_version.update(total_points=new_total_user_points_all_time_sum)

            def update_total_points_accumulated_for_all():
                current_model_updateable_version = Point_model.objects.filter(user_id=self.request.user.id)
                for model_obj in current_model_updateable_version:
                    # get all the models that are less than this date
                    ####if model_obj.date > date  start here 
                    this_user_point_models_total = current_model_updateable_version.filter(date__lt=model_obj.date).aggregate(Sum('total_points')) # re total it
                #sum_point_totals_below_this_date = all_dates_equal_to_or_less_than_this_date.aggregate(sum('total_points'))
                    if this_user_point_models_total['total_points__sum'] == None: # if this is the lowest date 
                        #update it 
                        # get this specific model via filter to update
                        model_to_update = current_model_updateable_version.filter(id=model_obj.id)
                        
                        model_to_update.update(up_to_date_total_points_accumulated=model_obj.total_points)
                    else:
                        sum_point_totals_including_this_date = this_user_point_models_total['total_points__sum'] + model_obj.total_points
                        model_to_update = current_model_updateable_version.filter(id=model_obj.id)

                        model_to_update.update(up_to_date_total_points_accumulated=sum_point_totals_including_this_date)

            update_user_sum_total_points()
            date_for_current_obj = form.instance.date # may be a problem if they change the date ???
            point_obj_for_this_form = Point_model.objects.filter(date=date_for_current_obj)
            point_obj_for_this_form.update(
                daily_point_goal=point_goal, total_points=total_points, 
                step_points=step_points, water_points=water_points, 
                clean_eating_points=clean_eating_points, workout_points=workout_points,
                date=date, sleep_points=sleep_points )
            update_total_points_accumulated_for_all() # do it after the model is updated

            def reset_goal_current_point_total():
                """Update goal object's current point total related to this input health object."""
                # just recall the goal_model counter
                all_point_goals = Point_goals.objects.filter(user=self.request.user)
                for obj in all_point_goals: # only get the point_input related to the user that set the goal 
                    if form.instance.date >= obj.goal_start_date and form.instance.date <= obj.goal_end_date:
                        obj.add_up_current_points_towards_goal()

            reset_goal_current_point_total()
            
        update_points()
        return super().form_valid(form)

        # see if i can grab the data here 

    def get_success_url(self):
        """Get the health input model's pk and return the user to the corresponding point model graph url. """
        pk_value = int(self.object.pk)  # there is a current difference of 16 between the User_point_input_model and Point Model pks
        return reverse('daily_point_graph', kwargs={'pk' : pk_value}) # this object pk will mimic the Point_model pk, they should always be equal, if not, this fails 

    def unanswered_challenge_invitations(self):
        """Check for challenge invitations,if found, create and send a message"""
        current_user_obj = self.request.user
        #all_invitations = current_user_obj.Invitation.all()  # without the set
        all_invitations_status_objects = current_user_obj.invitation_status_set.filter(status='idle')
        #all_invitations = current_user_obj.invitation_to_challenge_set.all()
        if all_invitations_status_objects:
            messages.add_message(self.request, messages.INFO, 
                                """Pending Invitation, to accept or reject
                                  go to Challenges -> Pending invitations""")

            
class All_time_leaderboard_view(LoginRequiredMixin, ListView):
    """A page showing all the users and their total points acumulated, ordered highest to lowest."""
    template_name = 'all_time_leader_board.html'
    model = Point_model

    # order the leaders based off of all time points 
    def all_time_point_leaders_in_order(self):
        """Order and return a queryset of users, by point total, highest to lowest. """
        most_points_order = My_custom_user.objects.order_by('-total_points')
        return most_points_order

    def unanswered_challenge_invitations(self):
        """Check for challenge invitations,if found, create and send a message"""
        current_user_obj = self.request.user
        #all_invitations = current_user_obj.Invitation.all()  # without the set
        all_invitations_status_objects = current_user_obj.invitation_status_set.filter(status='idle')
        #all_invitations = current_user_obj.invitation_to_challenge_set.all()
        if all_invitations_status_objects:
            messages.add_message(self.request, messages.INFO, 
                                 """Pending Invitation, to accept or 
                                  reject go to Challenges -> Pending invitations""")

            
class How_to_view(TemplateView):
    """A simple tutorial page, showing the viewer the function of the entire website."""
    template_name = "how_to.html"

    def unanswered_challenge_invitations(self):
        """Check for challenge invitations,if found, create and send a message"""
        current_user_obj = self.request.user
        #all_invitations = current_user_obj.Invitation.all()  # without the set
        all_invitations_status_objects = current_user_obj.invitation_status_set.filter(status='idle')
        #all_invitations = current_user_obj.invitation_to_challenge_set.all()
        if all_invitations_status_objects:
            messages.add_message(self.request, messages.INFO, 
                                """Pending Invitation, to accept or reject
                                 go to Challenges -> Pending invitations""")


class Rules_view(TemplateView):
    """A page showing the scoring rules for converting health data input into points """
    template_name = "rules.html"

    def unanswered_challenge_invitations(self):
        """Check for challenge invitations,if found, create and send a message"""
        current_user_obj = self.request.user
        #all_invitations = current_user_obj.Invitation.all()  # without the set
        all_invitations_status_objects = current_user_obj.invitation_status_set.filter(status='idle')
        #all_invitations = current_user_obj.invitation_to_challenge_set.all()
        if all_invitations_status_objects:
            messages.add_message(self.request, messages.INFO, 
                                 """Pending Invitation, to accept or reject 
                                 go to Challenges -> Pending invitations""")
