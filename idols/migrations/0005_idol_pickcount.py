# Generated by Django 4.0.10 on 2023-07-17 04:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('idols', '0004_remove_idol_pickcount'),
    ]

    operations = [
        migrations.AddField(
            model_name='idol',
            name='pickCount',
            field=models.PositiveBigIntegerField(default=0, editable=False),
        ),
    ]