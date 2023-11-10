# Generated by Django 4.2.7 on 2023-11-10 15:54

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Event",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("createdAt", models.DateTimeField(auto_now_add=True)),
                ("updatedAt", models.DateTimeField(auto_now=True)),
                ("name", models.TextField()),
                ("description", models.TextField()),
                ("date", models.DateField()),
                ("time", models.TimeField()),
                ("venue", models.TextField()),
                (
                    "department",
                    models.TextField(
                        choices=[
                            ("1", "Computer Engineering"),
                            ("2", "Mechanical Engineering"),
                            ("3", "Electronics & Telecommunication Engineering"),
                            ("4", "Electrical Engineering"),
                            ("5", "Information Technology"),
                            ("6", "Artificial Intelligence & Data Science"),
                            ("7", "First Year Engineering"),
                            ("8", "MBA"),
                        ]
                    ),
                ),
                ("link", models.URLField(blank=True, null=True)),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
