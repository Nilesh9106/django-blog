# Generated by Django 4.1.5 on 2023-03-27 06:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_alter_subscriber_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscriber',
            name='code',
            field=models.CharField(max_length=32, null=True),
        ),
    ]