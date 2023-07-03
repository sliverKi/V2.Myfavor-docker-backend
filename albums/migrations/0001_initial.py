# Generated by Django 4.0.10 on 2023-07-03 16:14

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('idols', '0005_remove_idol_idol_debut'),
        ('groups', '0003_group_group_debut_group_group_insta_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('album_name', models.CharField(blank=True, max_length=100, null=True)),
                ('album_cover', models.URLField(blank=True, max_length=100000, null=True)),
                ('release_date', models.DateField(default=datetime.date.today)),
                ('group_artists', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='albums', to='groups.group')),
                ('solo_artists', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='albums', to='idols.idol')),
            ],
        ),
    ]
