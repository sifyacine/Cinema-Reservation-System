# Generated by Django 4.1.10 on 2023-09-02 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone_number', models.CharField(max_length=20)),
                ('password', models.CharField(max_length=128)),
                ('email_verified', models.BooleanField(default=False)),
                ('phone_verified', models.BooleanField(default=False)),
            ],
        ),
    ]
