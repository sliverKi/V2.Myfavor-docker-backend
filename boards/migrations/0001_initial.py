# Generated by Django 4.0.10 on 2023-07-27 02:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Board',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(blank=True, choices=[('broadcast', 'BROADCAST'), ('event', 'EVENT'), ('release', 'RELEASE'), ('congrats', 'CONGRATS'), ('buy', 'BUY')], default='', max_length=15)),
            ],
            options={
                'verbose_name_plural': 'BoardType',
            },
        ),
    ]
