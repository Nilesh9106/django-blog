# Generated by Django 4.1.5 on 2023-03-27 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_subscriber_code'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=200)),
                ('name', models.CharField(max_length=200)),
                ('message', models.TextField()),
            ],
        ),
    ]
