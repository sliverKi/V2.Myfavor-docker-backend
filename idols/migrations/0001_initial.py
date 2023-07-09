# Generated by Django 4.0.10 on 2023-07-09 16:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('groups', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Idol',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idol_name_kr', models.CharField(default='', max_length=100)),
                ('idol_name_en', models.CharField(default='', max_length=100)),
                ('idol_profile', models.URLField(blank=True, max_length=10000, null=True)),
                ('is_solo', models.BooleanField(default=False)),
                ('idol_birthday', models.DateField(default=datetime.date.today)),
                ('has_schedules', models.BooleanField(default=False)),
                ('viewCount', models.PositiveBigIntegerField(default=0, editable=False)),
                ('group', models.ManyToManyField(blank=True, null=True, related_name='idols', to='groups.group')),
            ],
            options={
                'verbose_name_plural': 'Our_Idols',
            },
        ),
    ]
