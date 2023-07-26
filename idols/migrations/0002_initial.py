# Generated by Django 4.0.10 on 2023-07-27 02:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('idols', '0001_initial'),
        ('schedules', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='idol',
            name='idol_schedules',
            field=models.ManyToManyField(blank=True, related_name='idols', to='schedules.schedule'),
        ),
    ]
