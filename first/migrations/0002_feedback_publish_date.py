# Generated by Django 3.0.6 on 2020-10-10 11:19

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedback',
            name='publish_date',
            field=models.DateField(default=datetime.datetime(2020, 10, 10, 16, 49, 10, 390730)),
        ),
    ]
