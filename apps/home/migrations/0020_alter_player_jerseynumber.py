# Generated by Django 3.2.6 on 2021-12-25 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0019_alter_player_position'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='jerseyNumber',
            field=models.CharField(max_length=3),
        ),
    ]
