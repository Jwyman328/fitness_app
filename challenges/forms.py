from django import forms
from django.utils.timezone import now

from users.models import My_custom_user
from .models import Challenge, Invitation_to_challenge


class New_challenge_invitation_form(forms.ModelForm):

    class Meta:
        model = Invitation_to_challenge
        fields = ['title', 'start_date','end_date','challenge_health_field', 'invitees']  
    
    invitees = forms.ModelMultipleChoiceField(
        widget = forms.CheckboxSelectMultiple,
        queryset = My_custom_user.objects.all())

    def __init__(self,user_id, *args, **kwargs):
            super(New_challenge_invitation_form, self).__init__(*args, **kwargs)
            self.user_id = user_id
            self.fields['invitees'].queryset = My_custom_user.objects.exclude(id=self.user_id)
            #https://stackoverflow.com/questions/42492725/passing-request-to-django-form-still-shows-self-not-defined
            # how to override the field 

    challenge_health_field_choices = [
        ('sleep_points', 'Sleep'),('water_points', 'Water'), 
        ('clean_eating_points' ,'Clean Eating'), ('step_points', 'Steps'),
        ('total_points', 'Total Points'),('workout_points', 'Workout')]
    title =  forms.CharField()
    start_date = forms.DateField(
        initial=now,  help_text='year-month-day')
    end_date = forms.DateField(
        initial=now, help_text='year-month-day')
    challenge_health_field = forms.ChoiceField(
        choices=challenge_health_field_choices, label='Choices')
