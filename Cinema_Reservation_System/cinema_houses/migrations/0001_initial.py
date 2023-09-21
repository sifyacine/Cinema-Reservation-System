# Generated by Django 4.1.10 on 2023-09-18 11:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cinema',
            fields=[
                ('id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=200)),
                ('email_contact', models.EmailField(max_length=254)),
                ('rating', models.IntegerField(default=0)),
                ('phone_number', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Showtime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('movie_title', models.CharField(max_length=255)),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('is_available', models.BooleanField(default=True)),
                ('cinema_house', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cinema_houses.cinema')),
            ],
        ),
    ]
