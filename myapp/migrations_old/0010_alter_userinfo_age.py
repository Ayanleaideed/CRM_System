# Generated by Django 5.0.1 on 2024-01-31 06:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0009_rename_user_userinfo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='age',
            field=models.IntegerField(default=99999999999),
            preserve_default=False,
        ),
    ]
