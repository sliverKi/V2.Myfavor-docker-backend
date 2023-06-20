# Generated by Django 4.0.10 on 2023-06-20 15:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('idols', '0001_initial'),
        ('boards', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('ScheduleTitle', models.CharField(default='', max_length=150)),
                ('location', models.CharField(default='', max_length=150)),
                ('when', models.DateTimeField()),
                ('ScheduleType', models.ForeignKey(blank=True, max_length=150, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='schedules', to='boards.board')),
                ('participant', models.ManyToManyField(blank=True, max_length=150, related_name='schedules', to='idols.idol')),
            ],
            options={
                'verbose_name_plural': 'Idol-Schedules',
            },
        ),
    ]
