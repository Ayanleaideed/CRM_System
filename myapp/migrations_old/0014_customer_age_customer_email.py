# Generated by Django 5.0.1 on 2024-02-02 21:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0013_remove_userinfo_email_remove_userinfo_username_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='age',
            field=models.IntegerField(default=20),
        ),
        migrations.AddField(
            model_name='customer',
            name='email',
            field=models.CharField(default=20, max_length=255),
            preserve_default=False,
        ),
    ]
