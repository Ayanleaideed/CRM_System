# Generated by Django 5.0.1 on 2024-01-23 21:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_userprofile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='date_of_birth',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='last_login_date',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='registration_date',
        ),
    ]