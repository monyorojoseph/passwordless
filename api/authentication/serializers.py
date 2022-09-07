from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User
from dataclasses import fields
class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['username', 'password']