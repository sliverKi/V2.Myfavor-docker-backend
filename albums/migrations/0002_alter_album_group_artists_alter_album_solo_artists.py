# Generated by Django 4.0.10 on 2023-07-03 16:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0003_group_group_debut_group_group_insta_and_more'),
        ('idols', '0005_remove_idol_idol_debut'),
        ('albums', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='group_artists',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='albums_group', to='groups.group'),
        ),
        migrations.AlterField(
            model_name='album',
            name='solo_artists',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='albums_solo', to='idols.idol'),
        ),
    ]