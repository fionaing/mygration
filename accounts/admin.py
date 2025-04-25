from django.contrib import admin
from django.contrib.auth.models import User

from accounts.models import Profile, Warning

# Register your models here.
admin.site.register(Profile)
admin.site.register(Warning)