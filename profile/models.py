from django.db import models
from django.db.models.signals import post_save
from django.conf import settings

User = settings.AUTH_USER_MODEL

class FollowerRelation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)



class Profile(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    bio = models.CharField(max_length=100 , null= True, blank = True)
    location = models.CharField(max_length =150, null=True, blank=True)
    website = models.CharField(max_length=140,null=True,blank=True) 
    followers = models.ManyToManyField(User, related_name='following',blank=True)


    @property
    def following(self):
        return self.user.following.all().count()




def user_did_save(sender, instance, created, *args, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)

post_save.connect(user_did_save, sender=User)







# Create your models here.
