from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mfa_secret = models.CharField(max_length=32, blank=True, null=True)

    def __str__(self):
        return self.user.username
