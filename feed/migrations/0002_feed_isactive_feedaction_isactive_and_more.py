# Generated by Django 4.2.7 on 2023-11-11 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("feed", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="feed",
            name="isActive",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="feedaction",
            name="isActive",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="feedactioncomment",
            name="isActive",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="feedimage",
            name="isActive",
            field=models.BooleanField(default=True),
        ),
    ]
