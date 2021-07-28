from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.db import models
from .models import Tweets

class Tweet_Form(forms.ModelForm):
    class Meta:
        model = Tweets
        fields = ["content"]
class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields =['username','email']

       