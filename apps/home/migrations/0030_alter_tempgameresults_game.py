# Generated by Django 3.2.6 on 2022-01-03 03:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0029_auto_20220102_2207'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tempgameresults',
            name='game',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='home.game'),
        ),
    ]
