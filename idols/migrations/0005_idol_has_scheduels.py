# Generated by Django 4.0.10 on 2023-06-02 04:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('idols', '0004_alter_idol_idol_gender'),
    ]

    operations = [
        migrations.AddField(
            model_name='idol',
            name='has_scheduels',
            field=models.BooleanField(default=False),
        ),
    ]
