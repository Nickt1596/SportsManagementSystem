# Generated by Django 3.2.6 on 2021-12-29 00:51

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0020_alter_player_jerseynumber'),
    ]

    operations = [
        migrations.CreateModel(
            name='Goal',
            fields=[
                ('period', models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('OT', 'OT')], max_length=100)),
                ('timeScored', models.CharField(max_length=80)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('assistPrimary', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='Primary_Assist', to='home.playerstats')),
                ('assistSecondary', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='Secondary_Assist', to='home.playerstats')),
                ('goalScorer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Goal_Scorer', to='home.playerstats')),
            ],
        ),
    ]