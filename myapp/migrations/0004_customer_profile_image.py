# Generated by Django 5.0.1 on 2024-04-25 23:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("myapp", "0003_authenticationinfo"),
    ]

    operations = [
        migrations.AddField(
            model_name="customer",
            name="profile_image",
            field=models.ImageField(default="null", upload_to="profile_images/"),
            preserve_default=False,
        ),
    ]
