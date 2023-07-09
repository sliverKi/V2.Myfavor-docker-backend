# Generated by Django 4.0.10 on 2023-07-09 16:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('albums', '0001_initial'),
        ('groups', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='album',
            name='group_artists',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='albums_group', to='groups.group'),
        ),
    ]
