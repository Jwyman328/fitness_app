from django import forms 
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import My_custom_user

class Custom_User_Creation_form(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = My_custom_user
        fields = ['username', 'email', 'password1', 'password2']

        
class Custom_User_Change_form(UserChangeForm):
    class Meta:
        model = My_custom_user
        fields = UserChangeForm.Meta.fields
        
        