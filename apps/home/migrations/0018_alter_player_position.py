# Generated by Django 3.2.6 on 2021-12-25 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0017_playerstats_season'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='position',
            field=models.CharField(default='-', max_length=80),
        ),
    ]