# Generated by Django 5.0.1 on 2024-02-07 07:43

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="UserInfo",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        default=1,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Customer",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("email", models.CharField(max_length=255)),
                ("address", models.CharField(max_length=255)),
                ("age", models.BigIntegerField()),
                (
                    "phone_number",
                    models.CharField(blank=True, max_length=15, null=True),
                ),
                ("orders", models.BigIntegerField()),
                (
                    "vip_status",
                    models.CharField(
                        choices=[("platinum", "Platinum"), ("gold", "Gold")],
                        max_length=50,
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="myapp.userinfo"
                    ),
                ),
            ],
        ),
    ]
