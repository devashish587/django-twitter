# Generated by Django 3.2.3 on 2021-05-24 20:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tweets', '0008_alter_tweets_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tweets',
            old_name='User',
            new_name='user',
        ),
    ]
