# Generated by Django 3.2.6 on 2021-12-22 00:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0012_alter_season_currentseason'),
    ]

    operations = [
        migrations.AddField(
            model_name='playerstats',
            name='seasons',
            field=models.ManyToManyField(blank=True, null=True, to='home.Season'),
        ),
    ]
