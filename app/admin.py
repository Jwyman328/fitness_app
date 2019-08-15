from django.contrib import admin

# Register your models here. 
from .models import User_point_input_model, Point_model, Point_goals
""" 
class User_point_input_modelAdmin(admin.ModelAdmin):
    list_display = ('user',)
    def save_model(self, request, obj, form, change):
        if getattr(obj, 'user', None) is None:
            obj.user= request.user
        obj.save() """

admin.site.register(User_point_input_model)
admin.site.register(Point_model)
admin.site.register(Point_goals)
