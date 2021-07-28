from typing import Sequence, Text
from django.db import models
from django.db.models.base import Model
from django.db.models.deletion import CASCADE
from django.db.models.fields import FloatField, TextField
from django.db.models.fields.files import FileField
from django.conf import settings
from django.db.models.fields.related import ManyToManyField, OneToOneField
from django.db.models import Q
from profile.models import Profile


User = settings.AUTH_USER_MODEL

class TweetLike(models.Model):
    user= models.ForeignKey(User ,on_delete=models.CASCADE)
    tweets= models.ForeignKey("Tweets" ,on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)


    
class TweetLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tweet = models.ForeignKey("Tweets", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

class TweetsQuerySet(models.QuerySet):
    def by_username(self, username):
        return self.filter(user__username__iexact=username)

    def feed(self, user):
        profiles_exist = user.following.exists()
        followed_users_id = []
        if profiles_exist:
            followed_users_id = user.following.values_list("user__id", flat=True) # [x.user.id for x in profiles]
        return self.filter(
            Q(user__id__in=followed_users_id) |
            Q(user=user)
        ).distinct().order_by("-timestamp")

class TweetsManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return TweetsQuerySet(self.model, using=self._db)

    def feed(self, user):
        return self.get_queryset().feed(user)

# Create your models here.
class Tweets(models.Model):
    parent  = models.ForeignKey("self",null = True, on_delete=models.SET_NULL)
    user = models.ForeignKey(User ,on_delete=models.CASCADE )
    content = TextField( blank=True,null=True)
    likes = ManyToManyField(User,related_name ="tweet_like",blank=True,through=TweetLike)
    image  = FileField(upload_to ="images/" , blank=True,null= True )
    timestamp = models.DateTimeField(auto_now_add=True)
    
    objects = TweetsManager()
    class Meta:
        ordering  =["-id"]
        


    @property
    def is_retweet(self):
        return self.parent != None


