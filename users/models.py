from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Sum

# Create your models here.
class My_custom_user(AbstractUser):
    email = models.EmailField()
    total_points = models.PositiveIntegerField(default = 0, null = True, blank = True)


    def points_for_challenge(self, start_date, end_date, catagory):
        # get all the points by this user 
        params = [self, start_date, end_date, catagory]
        all_point_models = self.point_model_set.all()
        all_point_models = self.point_model_set.filter(date__gte = start_date).filter(date__lte = end_date).aggregate(Sum(catagory))
        total = 0
        for name, points in all_point_models.items():
            if points == None:
                points=0
            total += points

        return(total)
