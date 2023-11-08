# Generated by Django 4.2.5 on 2023-11-07 19:59

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Sensor_Data",
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
                ("temp", models.IntegerField(null=True)),
                ("humidity", models.IntegerField(null=True)),
                ("soil_moisture", models.IntegerField(null=True)),
                ("light_intensity", models.IntegerField(null=True)),
                ("create_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
