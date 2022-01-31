# Generated by Django 3.2.6 on 2022-01-31 16:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0010_alter_referee_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='player',
            old_name='altCaptain',
            new_name='isAltCaptain',
        ),
        migrations.RenameField(
            model_name='player',
            old_name='captain',
            new_name='isCaptain',
        ),
        migrations.AddField(
            model_name='player',
            name='email',
            field=models.CharField(blank=True, max_length=80, null=True),
        ),
        migrations.AddField(
            model_name='player',
            name='user',
            field=models.OneToOneField(blank=True, limit_choices_to={'type': 'PLAYER'}, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='scorekeeper',
            name='user',
            field=models.OneToOneField(blank=True, limit_choices_to={'type': 'SCOREKEEPER'}, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Captain',
            fields=[
                ('phoneNumber', models.CharField(max_length=80)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('player', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='home.player')),
                ('user', models.OneToOneField(blank=True, limit_choices_to={'type': 'CAPTAIN'}, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]