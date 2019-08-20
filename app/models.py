from django.db import models
from django.urls import reverse
from django.utils.timezone import now
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db.models import Sum

from users.models import My_custom_user
from users.models import My_custom_user


# Create your models here.
class User_point_input_model(models.Model):
    """Health Data in the total value of each specific catagory
    
    attributes: 
        user(obj): the current user object
        date(datefield): the date of the health actions
        Hours_of_sleep(int): the hours of sleep
        water_100oz(Boolean): True,if 100oz of water was drank 
        workout_intensity(int): value of 1-4 based on intensity of workout
        workout_amount_of_time(int): value in minutes of workout time
        steps(int): amount of total steps

    """ 
    user = models.ForeignKey(
               settings.AUTH_USER_MODEL,
               on_delete=models.CASCADE, 
               null=True, blank=True )   

    date = models.DateField(
               default=now, editable=True,
               help_text='year-month-day')

    Hours_of_sleep = models.PositiveIntegerField(default=0)
    Water_100oz = models.BooleanField(default=False)
    clean_eating = models.BooleanField(default=False)
    workout_intensity = models.PositiveIntegerField(
            default=0, 
            validators=[MaxValueValidator(4),MinValueValidator(0)],
            help_text="""input 0-4, None, light, moderate, 
            intense, super intense""") 

    workout_amount_of_time = models.PositiveIntegerField(
            default=0, verbose_name='Workout time (in minutes)')
    steps = models.PositiveIntegerField(default = 0)
    
    def __str__(self):
        """return the health input objects date as the representive string."""
        return  (str(self.date))

    def get_absolute_url(self):
        """Return the user to the homepage, once the health input object is created. """
        return reverse('home')

    def create_point_object(self):
        """Create corresponding point model object from calculations of the health input data."""
        def water_clean_eating_point_func(water_or_clean_eating_true_false):
            """ if the input is true, return 10
                
            Args: 
                water_or_clean_eating_true_false (boolean): True false, if the user 
                ate clean or drank 100oz of water.

            return: int:10 if param true

            """
            if water_or_clean_eating_true_false == True:
                return 10
            else:
                return 0 
        
        def point_goal_for_this_date():
            point_goal = 0
            all_point_goals = Point_goals.objects.filter(user=self.user)
            for obj in all_point_goals: 
            # only get the point_input related to the user that set the goal 
                
                if self.date >= obj.goal_start_date and self.date <= obj.goal_end_date:
                    point_goal = int(obj.point_goal)
                else:
                    pass
            return point_goal
                    
        sleep_points = self.Hours_of_sleep * 3.3
        date = self.date
        user = self.user
        workout_points = self.workout_intensity * (self.workout_amount_of_time * .2)
        clean_eating_points = water_clean_eating_point_func(self.clean_eating)
        water_points = water_clean_eating_point_func(self.Water_100oz)
        step_points = self.steps * .001
        total_points = (water_points + workout_points + sleep_points + 
                        clean_eating_points + step_points)              
        point_goal = point_goal_for_this_date()
        health_points_object = Point_model.objects.create(
                sleep_points=sleep_points, date=date,
                water_points=water_points, workout_points=workout_points,
                one_to_one_workout=self, total_points=total_points,
                clean_eating_points=clean_eating_points,
                user=user, daily_point_goal=point_goal )
        health_points_object.save()
    
    def update_points(self):

        def water_clean_eating_point_func(water_or_clean_eating_true_false):
            """ if the input is true, return 10
                
            Args: 
                water_or_clean_eating_true_false (boolean): True false, if the user 
                ate clean or drank 100oz of water.

            Return: int:10 if param true

            """
            if water_or_clean_eating_true_false == True:
                return 10
            else:
                return 0 

        sleep_points = self.Hours_of_sleep * 3.3
        date = self.date
        user = self.user
        workout_points = self.workout_intensity * (self.workout_amount_of_time * .2)
        clean_eating_points = water_clean_eating_point_func(self.clean_eating)
        water_points = water_clean_eating_point_func(self.Water_100oz)
        step_points = self.steps * .001
        total_points = water_points + workout_points + sleep_points + clean_eating_points + step_points
        
        the_object_to_update = Point_model.objects.filter(date=self.date)
        the_object_to_update.update(
                sleep_points=sleep_points, date=date, 
                water_points=water_points, workout_points=workout_points, 
                one_to_one_workout=self, total_points = total_points, 
                clean_eating_points=clean_eating_points,
                step_points=step_points,
                user=user )

    def save(self, *args, **kwargs):
        """Save the healh input health object, and after create a corresponding point obj."""
        is_new = True if not self.id else False # https://stackoverflow.com/questions/28264653/how-create-new-object-automatically-after-creating-other-object-in-django
        super(User_point_input_model, self).save(*args, **kwargs)
        if is_new:
            self.create_point_object() 


class Point_model(models.Model):
    """Point obj relating to a corresponing User_point_input_model object. 
    
    this object is generate automatically when the User_point_input_model
    object is create by the user.

    Attributes:
        sleep_points(int): sleep hrs* 3.3
        date(datefield): date of points
        water_points(int): int of 10, if the user drank 100oz of water
        workout_points(int): int based off of workouttime * workout intensity
        one_to_one_workout(obj): corresponding User_point_input_model
        total_points(int): sum of sleep_points, water_points, 
            workout_points,step points, and clean eating points
        clean_eating_points(int): int of 10, if the user ate clean
        step_points(int): total steps *.001
        user(obj): user that input User_point_input_model
        daily_point_goal(int): point total relating to a corresponing point_goal object
        up_to_date_total_points_accumulated(int) = total for all users point models from 
            this date and before this date.

    """
    sleep_points = models.PositiveIntegerField(default=0)
    date = models.DateField(default=now, editable=True)
    water_points = models.PositiveIntegerField(default=0)
    workout_points = models.PositiveIntegerField(default=0)
    one_to_one_workout = models.ForeignKey(
        User_point_input_model,on_delete=models.CASCADE ,
        null=True, blank=True  )                                    
    total_points = models.PositiveIntegerField(
        default=0, null=True, blank=True)
    clean_eating_points = models.PositiveIntegerField(default=0)
    step_points = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True, blank=True ) 
    daily_point_goal = models.PositiveIntegerField(
        default=0, null=True, blank=True) 
    up_to_date_total_points_accumulated = models.PositiveIntegerField(
        default=0, null=True, blank=True)

    def update_total_points_for_goal(self):
        """Update the correspong goal objs current point total."""
        all_point_goals = Point_goals.objects.filter(user=self.user) 
        # get all the goals for this user
        for obj in all_point_goals: # each start date obj
            if self.date >= obj.goal_start_date and self.date <= obj.goal_end_date:
                current_sum = int(obj.current_point_total_input)
                new_current_sum = current_sum + int(self.total_points)
                my_set_obj = all_point_goals.filter(id = obj.id) 
                # get a queryset so i can update 
                my_set_obj.update(current_point_total_input = new_current_sum)
                break
 
            else:
                pass

    def update_total_points_for_user(self):
        '''add points created to the users total points in this users model'''
        current_user_updateable_form = My_custom_user.objects.filter(id=self.user_id) 
        # filter for the current user 
        current_user = My_custom_user.objects.get(id=self.user_id)
        current_point_sum = current_user.total_points
        new_sum = current_point_sum + self.total_points
        current_user_updateable_form.update(total_points=new_sum)
    
    def total_points_accumulated(self):
        '''add points created to the users total points in this users model'''
        this_user_point_models = Point_model.objects.filter(user=self.user).filter(date__lt = self.date).aggregate(Sum('total_points'))
        if this_user_point_models['total_points__sum'] == None: # if this is the lowest date 
            self.up_to_date_total_points_accumulated = self.total_points
        else:
            sum_point_totals_including_this_date = this_user_point_models['total_points__sum'] + self.total_points
            self.up_to_date_total_points_accumulated = sum_point_totals_including_this_date
        
        def update_all_others_that_are_effected():
            '''any date that is created while dates later than
             it exist, then those later dates will have incorrect
             versions of there accumulated up to date total because it will
            not account for the new point input this function will reset those 
            later than this models date to their new correct accumulated total '''
            # get all the models of this user
            # then only get the models that have a higher date than this one 
            this_users_models = Point_model.objects.filter(user=self.user)
            # now get the ones that have a higher date than this one 
            above_this_models_date = this_users_models.filter(date__gt=self.date)
            for obj in above_this_models_date:
                obj_user_point_models = Point_model.objects.filter(user=self.user).filter(date__lte = obj.date).aggregate(Sum('total_points'))
                updateable_obj = Point_model.objects.filter(id=obj.id)
                updateable_obj.update(
                        up_to_date_total_points_accumulated=obj_user_point_models['total_points__sum'])
        
        update_all_others_that_are_effected()

    # when a point thing is made, update the goals point total 
    def save(self, *args, **kwargs):
        self.total_points_accumulated() 
        is_new = True if not self.id else False # https://stackoverflow.com/questions/28264653/how-create-new-object-automatically-after-creating-other-object-in-django
        super(Point_model, self).save(*args, **kwargs)
        if is_new:
            self.update_total_points_for_goal()
            self.update_total_points_for_user()



class Point_goals(models.Model):
    """A daily point total goal for a spanned time,start date - end date.
    
    Attributes:
        user(obj): the user who set the goal
        goal_start_date(datefield): the first day the goal starts
        goal_end_date(datefield): the last day the goal exists
        point_goal(int): the total point goal for each day in the date range
        goal_accomplished(str): a str represnting if the goal has been reached for the day
        points_needed_for_goal_achieved(int): the total points needed based off of
            number of days of the goal * point_goal
        current_point_total_input(int) = sum total of every single point obj
            that exists between goal_start_date and goal_end_date

    """
    user = models.ForeignKey(
            settings.AUTH_USER_MODEL, on_delete = models.CASCADE,
            null = True, blank=True ) 
    goal_start_date = models.DateField(
            default=now, editable=True, help_text='year-month-day')
    goal_end_date = models.DateField(
            default=now, editable=True, help_text='year-month-day')
    point_goal = models.PositiveIntegerField(
            default=50, help_text='Set Daily Point Goal')
    goal_accomplished = models.TextField(
            default='no', null=True, blank=True)
    points_needed_for_goal_achieved = models.PositiveIntegerField(
            default=1, null=True, blank=True)
    current_point_total_input = models.PositiveIntegerField(
            default=0, null=True, blank=True)

    def points_needed_to_reach_goal(self):
        """Calculate and update the points needed to acomplish this goal.
        
        points needed to acomplish goal = days in goal * points per day

        """
        #date_format = "%Y/%m/%d"
        date_time_start = self.goal_start_date
        date_time_end = self.goal_end_date
        
        number_of_days = self.goal_end_date - self.goal_start_date  
        number_of_days = number_of_days.days
        days_times_daily_points = int(number_of_days) * self.point_goal

        current_goal_obj = Point_goals.objects.filter(id=self.id)
        current_goal_obj.update(
                points_needed_for_goal_achieved=days_times_daily_points)
    
    def remove_goal_from_individual_point_inputs(self):
        """Update all point objects relating to goal object to 0. """
        # find all individual days that this goal was set for 
        # update thier goal count to 0
        # get a date range, can do with a filter, then can update an entire filter 
        point_obj_in_goal_date_range = Point_model.objects.filter(date__range=[self.goal_start_date, self.goal_end_date])
        point_obj_in_goal_date_range.update(daily_point_goal=0.0)
    
    def add_goal_field_to_point_object(self):
        """Add the daily point goal to each point model that falls between the goals start and end date."""
        for obj in Point_model.objects.filter(user=self.user): # only get the point_input related to the user that set the goal 
            if obj.date >= self.goal_start_date and obj.date <= self.goal_end_date:                
                updatable_point_model_filter = Point_model.objects.filter(id=obj.id)
                updatable_point_model_filter.update(daily_point_goal=self.point_goal)

    def add_up_current_points_towards_goal(self):
        """Add the current points that exist towards this goal."""
        current_sum_points_in_goal_date_range = 0
        point_obj_for_user = Point_model.objects.filter(user=self.user)
        point_obj_in_goal_date_range = point_obj_for_user.filter(date__range=[self.goal_start_date,self.goal_end_date])
        for obj in point_obj_in_goal_date_range:
            current_sum_points_in_goal_date_range += obj.total_points
        # now update it 
        current_goal_obj = Point_goals.objects.filter(id=self.id)
        current_goal_obj.update(
            current_point_total_input=int(current_sum_points_in_goal_date_range)  )

    def save(self, *args, **kwargs):
        """Save the current goal and after call corresponding functions
        
        corresonding functions: add_goal_field_to_point_object,
            points_needed_to_reach_goal, add_up_current_points_towards_goal

         """
        date_conflict = False
        for obj in Point_goals.objects.filter(user=self.user):
            if self.goal_start_date >= obj.goal_start_date and self.goal_start_date <= obj.goal_end_date: # if the start date is inside preexisting goal
                date_conflict = True
            else:
                pass
        if date_conflict:
            pass
        else:
            is_new = True if not self.id else False # https://stackoverflow.com/questions/28264653/how-create-new-object-automatically-after-creating-other-object-in-django
            super(Point_goals, self).save(*args, **kwargs)
            if is_new:
                self.add_goal_field_to_point_object()
                self.points_needed_to_reach_goal()
                self.add_up_current_points_towards_goal()

    def delete(self, *args, **kwargs):
        self.remove_goal_from_individual_point_inputs()
        super(Point_goals, self).delete(*args, **kwargs)


