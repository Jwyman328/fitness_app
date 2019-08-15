from django.contrib import admin
from .models import My_custom_user
from django.contrib.auth.admin import UserAdmin
from .forms import Custom_User_Change_form, Custom_User_Creation_form

# Register your models here.
class Custom_user_admin(UserAdmin):
    form = Custom_User_Change_form
    add_form = Custom_User_Creation_form
    list_display = ['username','email']
    model = My_custom_user

admin.site.register(My_custom_user, Custom_user_admin)
