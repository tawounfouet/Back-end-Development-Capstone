# Generated by Django 5.0.2 on 2024-02-08 15:34

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("concert", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="concert",
            name="city",
            field=models.CharField(default="", max_length=255),
        ),
        migrations.AddField(
            model_name="concert",
            name="concert_name",
            field=models.CharField(default="", max_length=255),
        ),
        migrations.AddField(
            model_name="concert",
            name="date",
            field=models.DateField(default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name="concert",
            name="duration",
            field=models.IntegerField(default=0),
        ),
    ]