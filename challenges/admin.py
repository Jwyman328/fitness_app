from django.contrib import admin

# Register your models here.
from .models import Challenge, Invitation_to_challenge, Invitation_status
admin.site.register(Challenge)
admin.site.register(Invitation_to_challenge)
admin.site.register(Invitation_status)

