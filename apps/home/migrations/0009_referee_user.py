# Generated by Django 3.2.6 on 2022-01-28 15:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0008_alter_scorekeeper_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='referee',
            name='user',
            field=models.OneToOneField(limit_choices_to={'type': 'REFEREE'}, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
