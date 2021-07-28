# Generated by Django 3.2.3 on 2021-05-25 16:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tweets', '0009_rename_user_tweets_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='tweets',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='TweetLike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('tweets', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tweets.tweets')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='tweets',
            name='likes',
            field=models.ManyToManyField(null=True, related_name='tweet_like', through='tweets.TweetLike', to=settings.AUTH_USER_MODEL),
        ),
    ]
