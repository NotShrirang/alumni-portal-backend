# Generated by Django 4.2.7 on 2023-11-10 15:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("donation", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="donation",
            options={"managed": True, "verbose_name_plural": "donation"},
        ),
        migrations.AlterModelTable(
            name="donation",
            table="donation",
        ),
    ]
