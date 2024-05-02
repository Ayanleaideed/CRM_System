# Generated by Django 5.0.1 on 2024-05-02 02:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("myapp", "0004_customer_profile_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customer",
            name="profile_image",
            field=models.ImageField(
                default='<i class="bi bi-file-person-fill"></i>',
                upload_to="profile_images/",
            ),
        ),
    ]
