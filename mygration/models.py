from django.db import models
from django.contrib.auth.models import User

"""
Info relating to a plan.
"""
class Plan(models.Model):
    id = models.AutoField(primary_key=True) # automatically created id
    name = models.CharField(max_length=255) # plan name
    user = models.ForeignKey(User, on_delete=models.CASCADE) # user who created plan
    location = models.CharField(max_length=255) #txt field for location
    date = models.DateTimeField(auto_now_add=True) # set date
    description = models.TextField() # txt field for description
    joined = models.CharField(max_length=255) # txt field to add whos joined
    image = models.ImageField(upload_to='plan_images/')

    def __str__(self):
        return str(self.id) + ' - ' + self.name

"""
Created when a user joins another person’s plan
"""
class Joined(models.Model):
    id = models.AutoField(primary_key=True) # automatically created id
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)  # plan its associated w/ - plan id
    user = models.ForeignKey(User, on_delete=models.CASCADE) # user who created plan - user id

    def __str__(self):
        return str(self.id) + ' - ' + self.plan.name

"""
Comments made on plan.
"""
class Comment(models.Model):
    id = models.AutoField(primary_key=True) # automatically created id
    user = models.ForeignKey(User, on_delete=models.CASCADE) # user that made review - user id
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE) # plan its associated w/ - plan id
    comment = models.CharField(max_length=255) # review text, max 255 chars
    date = models.DateTimeField(auto_now_add=True) # date review made

    def __str__(self):
        return str(self.id) + ' - ' + self.plan.name