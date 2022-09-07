from django.db import models
from django.contrib.auth.models import User

class User(models.Model):
    username=models.OneToOneField(User, on_delete=models.CASCADE)
    password=models.CharField(max_length=50)
    auth_token=models.CharField(max_length=100)
    is_verified=models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
        

