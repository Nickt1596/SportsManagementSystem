# Generated by Django 3.2.6 on 2022-01-17 23:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_rename_seasoncomplted_season_seasoncompleted'),
    ]

    operations = [
        migrations.AddField(
            model_name='gameresult',
            name='quickReport',
            field=models.BooleanField(default=False),
        ),
    ]
