# Generated by Django 4.1.7 on 2023-06-02 17:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0008_rename_idol_groups_member'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='groups',
            name='is_solo',
        ),
    ]
