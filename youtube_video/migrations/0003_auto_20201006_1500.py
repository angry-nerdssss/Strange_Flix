# Generated by Django 2.2.3 on 2020-10-06 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('youtube_video', '0002_auto_20201006_1453'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='description',
            field=models.TextField(max_length=500),
        ),
    ]
