# Generated by Django 2.2.6 on 2019-11-03 19:58

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Challenge',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('start_date', models.DateField(default=django.utils.timezone.now, help_text='year-month-day')),
                ('end_date', models.DateField(default=django.utils.timezone.now, help_text='year-month-day')),
                ('challenge_health_field', models.CharField(choices=[('sleep_points', 'Sleep'), ('water_points', 'Water'), ('clean_eating_points', 'Clean Eating'), ('step_points', 'Steps'), ('total_points', 'Total Points'), ('workout_points', 'Workout')], default='total_points', max_length=10000)),
            ],
        ),
        migrations.CreateModel(
            name='Invitation_status',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('idle', 'idle'), ('accepted', 'accepted'), ('rejected', 'rejected')], default='idle', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Invitation_to_challenge',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField(default=django.utils.timezone.now, help_text='year-month-day')),
                ('end_date', models.DateField(default=django.utils.timezone.now, help_text='year-month-day')),
                ('challenge_health_field', models.CharField(choices=[('sleep_points', 'Sleep'), ('water_points', 'Water'), ('clean_eating_points', 'Clean Eating'), ('step_points', 'Steps'), ('total_points', 'Total Points'), ('workout_points', 'Workout')], default='total_points', max_length=10000)),
                ('username_of_invitor', models.CharField(blank=True, max_length=100, null=True)),
                ('title', models.CharField(max_length=200)),
            ],
        ),
    ]
