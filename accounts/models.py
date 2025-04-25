from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField()

    def __str__(self):
        return self.user.username

class Warning(models.Model):
    class Categories(models.TextChoices):
        SPAM = "Spam", "Spam"
        BEHAVIOR = "Inappropriate Behavior", "Inappropriate Behavior"
        TOPIC = "Off Topic", "Off Topic"

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=50, choices=Categories, default=Categories.BEHAVIOR)
    warning = models.TextField()