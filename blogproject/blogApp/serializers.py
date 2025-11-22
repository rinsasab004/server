from rest_framework import serializers
from django.contrib.auth.models import User
from blogApp.models import ProfileModel



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','username','email','password']

class ProfileSerialixer(serializers.ModelSerializer):
    id=serializers.IntegerField(read_only=True)
    user=UserSerializer(read_only=True)
    followers=serializers.CharField(read_only=True)
    class Meta:
        model=ProfileModel
        fields="__all__"
