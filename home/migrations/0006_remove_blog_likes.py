# Generated by Django 4.1.5 on 2023-03-14 04:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_blog_likes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blog',
            name='likes',
        ),
    ]