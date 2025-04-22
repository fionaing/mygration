from django.contrib import admin
from .models import Plan, Joined, Comment

admin.site.register(Plan)
admin.site.register(Joined)
admin.site.register(Comment)