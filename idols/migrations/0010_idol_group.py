# Generated by Django 4.1.7 on 2023-06-05 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0011_rename_groups_group'),
        ('idols', '0009_rename_has_scheduels_idol_has_schedules_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='idol',
            name='group',
            field=models.ManyToManyField(to='groups.group'),
        ),
    ]
