# Generated by Django 3.2.6 on 2022-01-31 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0011_auto_20220131_1105'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='captain',
            name='phoneNumber',
        ),
        migrations.AddField(
            model_name='player',
            name='phoneNumber',
            field=models.CharField(blank=True, max_length=80, null=True),
        ),
    ]
