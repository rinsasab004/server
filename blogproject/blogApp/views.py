from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from blogApp.serializers import UserSerializer,ProfileSerialixer
from blogApp.models import ProfileModel
from rest_framework import authentication,permissions

# Create your views here.

class UserView(ModelViewSet):
    queryset=User.objects.all()
    serializer_class=UserSerializer

    def create(self,request,**kwargs):
        serializer=UserSerializer(data=request.data)
        if serializer.is_valid():
            User.objects.create_user(**serializer.validated_data)
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
        
class ProfileView(ModelViewSet):
    serializer_class=ProfileSerialixer
    queryset=ProfileModel
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def perform_create(self, serializer):
        return super().perform_create(serializer)
        
