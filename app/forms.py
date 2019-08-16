from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model

from .models import Point_goals, User_point_input_model

class Point_goals_form(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')  
        # To get request.user. Do not use kwargs.pop('user', None) due to potential security hole
        super(Point_goals_form, self).__init__(*args, **kwargs)

    class Meta:
        model = Point_goals
        fields = ['point_goal','goal_start_date','goal_end_date']  
    
    def clean_goal_start_date(self):
        "validate here"
        goal_start_date_passed = self.cleaned_data.get('goal_start_date')
        this_user = self.user
        what_i_want = 'today'

        for obj in Point_goals.objects.filter(user = this_user):
            if (goal_start_date_passed >= obj.goal_start_date and
                    goal_start_date_passed <= obj.goal_end_date): # if the start date is inside preexisting goal
                raise forms.ValidationError(("Sorry, a goal already exists for some of these dates, choose different dates, or delete the other goal"))
            else:
                pass
        return goal_start_date_passed


class Health_input_form(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')  # To get request.user. Do not use kwargs.pop('user', None) due to potential security hole

        super(Health_input_form, self).__init__(*args, **kwargs)

    class Meta:
        model = User_point_input_model
        fields = ['date', 'Hours_of_sleep','Water_100oz',
                  'clean_eating', 'workout_intensity', 
                  'workout_amount_of_time', 'steps']

    def clean_date(self):
        "validate here"
        date = self.cleaned_data.get('date')
        this_user = self.user

        for obj in User_point_input_model.objects.filter(user = this_user):
            if date == obj.date: # if the start date is inside preexisting goal
                raise forms.ValidationError(("""Sorry, there is already an input 
                                            for this date, you can go update it 
                                            if you have extra data to input"""))
            else:
                pass
        return date