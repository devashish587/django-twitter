from django.http import response
  
from django.shortcuts import render, redirect
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from .serializer import ProfileValidateSerializer
from typing import Text
import datetime
from django.http.response import HttpResponse,JsonResponse,Http404,HttpResponseRedirect
from django.shortcuts import render
from.serializer import ProfileActionSerializer
from .models import Tweets, User
from django.http import HttpResponseRedirect
from profile.models import Profile
from .forms import Tweet_Form
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import SerializeTweetClass
from rest_framework.decorators import action, api_view, permission_classes
from .serializer import SerializerActionClass
from rest_framework.authentication import SessionAuthentication
from .serializer  import  SerializerReadOnlyClass
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .serializer import ProfileViewSerializer
import requests
import json
from.forms import SignupForm
User=get_user_model()








# Create your views here.
def home(request):
    return HttpResponse("<h1> hello world</h1")


def account(request, data_id ,):
    Tweets.objects.create(text =data_id)
    
    return HttpResponse(f"ho gya{data_id}")


def create(request , id ):
    obj = Tweets.objects.get(id = id)
    data ={
        "id":id
    }
    status = 200
    try:
        value  = obj.content
        data["content"] =value
    
    except:
        data["message"] ="not found"
        status = 400

    return JsonResponse(data , status = status)


@login_required(login_url='login/')
def index(request):
       user = request.user
       list ={"user":user}
    
       return render(request , "index.html",list)

@api_view(["GET"])
def tweets_list(request):
    if not request.user.is_authenticated:
        return Response({},status=403)
    
    else:
        list =Tweets.objects.feed(request.user)
        serializer =  SerializerReadOnlyClass(list , many=True)
        return Response(serializer.data)

@csrf_exempt
def register(request):
    if request.method =="POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=True)
            user.set_password(form.cleaned_data["password1"])
            login(request ,user)
            Profile.objects.get_or_create(user=user)
            return redirect("/")
        elif not form.is_valid():
            return render(request,'register.html', {"error":form.errors})
    
    
    else:
       return render(request,'register.html' )



@api_view(['POST'])
def tweets_adder(request):
   serializer = SerializeTweetClass(data = request.data )
   if request.is_ajax():
      if serializer.is_valid(raise_exception=True) :
             serializer.save(user = request.user)
             dict = serializer.data
             dict['user']={'username':request.user.username}
             now  = datetime.datetime.now()
             dict['timestamp'] =[now]
             return Response(dict)
            
            

   else:
        if serializer.is_valid(raise_exception=True) :
             print('hello world ')
             serializer.save(user = request.user)
             serializer =  SerializerReadOnlyClass(list , many=True)
             return Response(serializer.data,status=201)


@api_view(['POST'])
def tweet_action_controller(request):
     if request.is_ajax():
        serializer = SerializerActionClass(data =request.data)
        if serializer.is_valid(raise_exception=True):
            id = serializer.data.get("id")
            action = serializer.data.get("action")
            if action =="like":
                obj = Tweets.objects.get(id = id )
                obj.likes.add(request.user)
                return Response(status=200)
            if action =="unlike":
                obj = Tweets.objects.get(id = id )
                obj.likes.remove(request.user)
                return Response(status=200)
            if action=="retweet":
                obj  = Tweets.objects.get(id = id )
                content = obj.content
                Tweets.objects.create(user = request.user, parent = obj, content=content)
                return Response(status=200)
@csrf_exempt
def logins(request):
    if request.method =="POST":
        fm = AuthenticationForm(request=request,data=request.POST)
        if fm.is_valid():
            username  = fm.cleaned_data['username']
            password = fm.cleaned_data['password']
            user = authenticate(username = username,password =password)
            login(request,user)
            return HttpResponseRedirect("/")

        if not fm.is_valid():
             form = AuthenticationForm()
             return render(request,"login.html",{"form":form ,"caption":"please type password and username correctly"})
    else:
        form = AuthenticationForm()
        return render(request, "login.html",{"form":form})


@api_view(["POST"])
def search_profile(request):
    usernames= request.data.get("username")
    profile =  Profile.objects.filter(user__username=usernames)
    profile =profile.first()
    serializer=  ProfileViewSerializer(profile)
    dict = serializer.data
    if profile.followers.all() != "null":
        if request.user in profile.followers.all():
           status = "Following"
    if profile.followers.all() =="null":
        status ="Follow"
    else:
        status="Follow"
    dict["status"] =status
    return Response(dict)



@api_view(["POST"])
def search_profile_username(request):
    try:
        usernames= request.data.get("username")
        profile =  Profile.objects.filter(user__username=usernames)
        profile =profile.first()
        serializer=  ProfileViewSerializer(profile)
        dict = serializer.data
        if request.user in profile.followers.all():
            status = "Following"
        else:
            status = "Follow"
        dict["status"] =status
        return Response(dict ,status = 200)
    except:
        return Response({},status=404)




@api_view(['POST'])
def news_feed(request):
       response = requests.get('https://newsapi.org/v2/top-headlines?' +
          'country=us&' +
          'apiKey=a2500047a10247f09ee6c42ed4922452')
       json_response = response.json()
       return Response(json_response)

@api_view(['POST'])
def get_username_tweets(request):
     if request.is_ajax():
        that_person = request.data["usernames"]
        username_Tweets = Tweets.objects.filter(user__username=that_person)
        serializer =  SerializerReadOnlyClass(username_Tweets, many=True)
        return Response(serializer.data)


@api_view(['POST'])
def follow_status(request):
    print(request.data)
    serializer  = ProfileActionSerializer(data =request.data)
    
    if serializer.is_valid():
        username_to_be_follow= serializer.data.get("username")
        status = serializer.data.get("status")
        if status=="Follow":
            profile_user_to_be_follow = Profile.objects.filter(user__username =username_to_be_follow)
            user_to_be_follow = profile_user_to_be_follow.first()
            user_to_be_follow.followers.add(request.user)
            return Response({},status =200)
        if status=="Following":
             profile_user_to_be_unfollow = Profile.objects.filter(user__username =username_to_be_follow)
             user_to_be_unfollow = profile_user_to_be_unfollow.first()
             user_to_be_unfollow.followers.remove(request.user)
             return Response({},status =200)



def profile_update(request):
    print(request.POST)
    if request.method =="POST":
        print(request.POST)
        data = request.POST
        locations = data['Location']
        websites = data['Website']
        bios  = data['bio']
        if len(websites)> 30:
            return render(request ,"profile.html",{"error":"your websites exceeds words limit"})
        if len(bios) >100:
            return render(request ,"profile.html",{"error":"your bio exceeds words limit"})
        if len(locations)>30:
            return render(request,"profile.html",{"error":"your location exceeds words limit"})
        else:
            user  = Profile.objects.filter(user = request.user)
            user.update(user=request.user,bio= bios,website=websites,location=locations,)
            return redirect("/")

    if request.method =="GET":
        Profiles= Profile.objects.filter(user= request.user)
        return render(request,"profile.html",{"profile":Profiles})



def logout_view(request, *args, **kwargs):
    if request.method == "POST":
        logout(request)
        return redirect("/login")
    return render(request,"logout.html")




    
     


    


          

    
                  
 
        



        


