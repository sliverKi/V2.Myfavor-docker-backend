# Generated by Django 4.0.10 on 2023-06-25 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0002_initial'),
        ('idols', '0003_idol_viewcount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='idol',
            name='group',
            field=models.ManyToManyField(blank=True, null=True, related_name='idols', to='groups.group'),
        ),
    ]