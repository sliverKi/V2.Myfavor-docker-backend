# Generated by Django 4.0.10 on 2023-07-27 02:38

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('idols', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Solo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('enter', models.CharField(blank=True, max_length=40, null=True)),
                ('solo_profile', models.URLField(blank=True, max_length=100000, null=True)),
                ('solo_debut', models.DateField(default=datetime.date.today)),
                ('solo_insta', models.URLField(blank=True, max_length=10000, null=True)),
                ('solo_youtube', models.URLField(blank=True, max_length=10000, null=True)),
                ('member', models.ForeignKey(blank=True, max_length=40, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='idol_solo', to='idols.idol')),
            ],
            options={
                'verbose_name_plural': 'Idols_Solo',
            },
        ),
    ]
