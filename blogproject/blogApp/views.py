from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from blogApp.serializers import UserSerializer,ProfileSerializer,PostSerializer,CommentSerializer
from blogApp.models import ProfileModel,PostModel,CommentModel
from rest_framework import authentication,permissions
from rest_framework.decorators import action

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
    serializer_class=ProfileSerializer
    queryset=ProfileModel
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        return super().perform_create(serializer)
    
    @action(methods=['POST'],detail=True)
    def add_follower(self,request,*args,**kwargs):
        profile_to_follow=ProfileModel.objects.get(id=kwargs.get("pk"))
        user_following=request.user
        profile_to_follow.followers.add(user_following)
        return Response({'msg':'followed'})
    
    @action(methods=['GET'],detail=True)
    def list_followers(self,request,*args,**kwargs):
        profile=ProfileModel.objects.get(id=kwargs.get("pk"))
        followers_list=profile.followers.all()
        serializer=UserSerializer(followers_list,many=True)
        return Response(data=serializer.data)
    
class PostView(ModelViewSet):
    serializer_class=PostSerializer
    queryset=PostModel.objects.all()
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def perform_create(self,serializer):
        serializer.save(user=self.request.user)
        return super().perform_create(serializer)
    
    @action(methods=['POST'],detail=True)
    def add_like(self,request,*args,**kwargs):
        post_to_like=PostModel.objects.get(id=kwargs.get("pk"))
        user=request.user
        post_to_like.likes.add(user)
        return Response({'msg':'liked'})
    
    @action(methods=['POST'],detail=True)
    def add_comment(self,request,*args,**kwargs):
        post=PostModel.objects.get(id=kwargs.get("pk"))
        user=request.user
        serializer=CommentSerializer(data=request.data)
        if serializer.is_valid():
            CommentModel.objects.create(**serializer.validated_data,user=user,post=post)
            return Response(data=serializer.data)
        
    @action(methods=['GET'],detail=True)
    def comments_list(self,request,*args,**kwargs):
        post=PostModel.objects.get(id=kwargs.get("pk"))
        comments=CommentModel.objects.filter(post=post)
        serializer=CommentSerializer(comments,many=True)
        return Response(data=serializer.data)
    

