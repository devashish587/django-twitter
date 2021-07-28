
from django.contrib import admin
from django.urls import path
from django.urls.resolvers import URLPattern
from . import views





urlpatterns =[
    path('hello' , views.home , name="wwe"),
    path("name/<int:data_id>",views.account , name="Account_Creation"),
    path("about/<int:id>", views.create , name= "about" ),
    path("tweets_list/", views.tweets_list),
    path("adding_tweets", views.tweets_adder),
    path("like-controller",views.tweet_action_controller),
    path("profile/", views.search_profile),
    path("news-feed/",views.news_feed),
    path("username-tweets/",views.get_username_tweets),
    path("follow_controller/", views.follow_status),
    path("view-profile/" ,views.search_profile_username),
    ]

