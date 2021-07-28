
from re import T
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import fields
from django.shortcuts import resolve_url
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from .models import Tweets
from django.contrib.auth import get_user_model
from profile.models import Profile
User = get_user_model()

TWEET_ACTION_OPTIONS=["like", "unlike","retweet"]

class SerializerUserNameReadOnlyClass(serializers.ModelSerializer):
    class Meta:
        model = User
        fields  =["username" ,"date_joined"]


class SerializeTweetClass(serializers.ModelSerializer):
    class Meta:
        model = Tweets
        fields = ["content" ,"id", "likes","timestamp" ]

    def get_likes(self , obj):
            if obj.likes =="null":
              return 0
            else:
                return obj.likes.count()

   


    def validate_content(self, value):
            if len(value) >200:
                raise serializers.ValidationError("this tweet is too long")
            else:
                return value




class SerializerActionClass(serializers.Serializer):
    id = serializers.IntegerField()
    action = serializers.CharField()
    content = serializers.CharField(required= False)

    def validate_action(self,value):
        value= value.lower().strip()   
        if not value in TWEET_ACTION_OPTIONS:
            raise serializers.ValidationError("this is not correct method ")
        else:
            return value 

class SerializerReadOnlyClass(serializers.ModelSerializer):
     likes = serializers.SerializerMethodField(read_only= True)
     parent = SerializeTweetClass(read_only=True)
     user = SerializerUserNameReadOnlyClass(read_only = True)

     class Meta:
         model = Tweets
         fields = [ "user","id" , "content", "is_retweet" ,"parent" , "likes","timestamp"]

     def get_likes(self, obj):
          return obj.likes.count()


class ProfileViewSerializer(serializers.ModelSerializer):
    user = SerializerUserNameReadOnlyClass(read_only = True)
    followers = SerializerMethodField(read_only = True)

    class Meta:
       model = Profile
       fields =['user','bio','location','website','followers' ,'following']


    def get_followers(self,obj):
      if obj.followers =="null":
          return 0
      else:
          return obj.followers.count()

    
class ProfileActionSerializer(serializers.Serializer):
    username = serializers.CharField()
    status = serializers.CharField()



class ProfileValidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields =["bio","website", "location"]

    def validate_bio(self, value):
        if len(value)> 100:
            raise serializers.ValidationError("Your  bio exceed words limit ")
        else:
            return value
    def validate_website(self, value):
        if len(value)> 40:
            raise serializers.ValidationError("Your website exceeds word limit  ")
        else:
            return value
    def validate_location (self, value):
        if len(value)> 40:
            raise serializers.ValidationError("Your location exceeds word limit  ")
        else:
            return value
