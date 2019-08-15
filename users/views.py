from django.shortcuts import render
from django.views.generic import CreateView
from .models import My_custom_user
from .forms import Custom_User_Creation_form


# Create your views here.

class Signup_user(CreateView):
    #model = My_custom_user
    template_name = 'signup.html'
    form_class = Custom_User_Creation_form
    success_url = '/accounts/login'
    