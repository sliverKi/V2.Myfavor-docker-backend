# Generated by Django 4.0.10 on 2023-07-22 02:23

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_remove_user_selected_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='when',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
