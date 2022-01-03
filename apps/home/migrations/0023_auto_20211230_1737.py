# Generated by Django 3.2.6 on 2021-12-30 22:37

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0022_penalty'),
    ]

    operations = [
        migrations.AddField(
            model_name='teamstats',
            name='ties',
            field=models.IntegerField(default=0),
        ),
        migrations.CreateModel(
            name='GameResult',
            fields=[
                ('winType', models.CharField(choices=[('Regulation', 'REG'), ('Overtime', 'OT'), ('Shootout', 'SO'), ('Tie', 'TIE')], max_length=100)),
                ('winnerScore', models.IntegerField(default=0)),
                ('loserScore', models.IntegerField(default=0)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('game', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='home.game')),
                ('losingTeam', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Losing_Team', to='home.team')),
                ('winningTeam', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Winning_Team', to='home.team')),
            ],
        ),
    ]
