# Generated by Django 4.1.7 on 2023-03-29 03:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_user_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.EmailField(blank=True, max_length=254, null=True, unique=True),
        ),
    ]
