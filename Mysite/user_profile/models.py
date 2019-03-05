from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Profile(models.Model):
    GENDER_CHOICES = (('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other'))
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    gender = models.TextField(blank=True, choices=GENDER_CHOICES)
    birth_date = models.DateField(blank=True, auto_now=False, auto_now_add=False, null=True)
    avatar_url = models.CharField(max_length=500, blank=True, null=True)
    avatar_path = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return str(self.user.username)
