# Generated by Django 4.1.10 on 2023-09-22 14:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_userprofile_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='user',
        ),
    ]