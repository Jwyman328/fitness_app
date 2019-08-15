from django.contrib import admin

# Register your models here. 
from .models import User_point_input_model, Point_model, Point_goals

admin.site.register(User_point_input_model)
admin.site.register(Point_model)
admin.site.register(Point_goals)
