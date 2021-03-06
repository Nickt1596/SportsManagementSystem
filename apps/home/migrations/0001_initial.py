# Generated by Django 3.2.6 on 2022-01-09 04:23

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Division',
            fields=[
                ('name', models.CharField(max_length=50)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('gameType', models.CharField(choices=[('Exhibition', 'Exhibition'), ('Regular Season', 'Regular Season'), ('Playoff', 'Playoff'), ('Championship', 'Championship')], max_length=100)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('firstName', models.CharField(max_length=80)),
                ('lastName', models.CharField(max_length=80)),
                ('jerseyNumber', models.CharField(max_length=3)),
                ('position', models.CharField(blank=True, max_length=80, null=True)),
                ('captain', models.BooleanField(default=False)),
                ('altCaptain', models.BooleanField(default=False)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Referee',
            fields=[
                ('name', models.CharField(max_length=80)),
                ('phoneNumber', models.CharField(max_length=80)),
                ('email', models.CharField(max_length=80)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Rink',
            fields=[
                ('name', models.CharField(max_length=80)),
                ('streetAddress', models.CharField(max_length=150)),
                ('city', models.CharField(max_length=80)),
                ('state', models.CharField(max_length=80)),
                ('zip', models.CharField(max_length=80)),
                ('phoneNumber', models.CharField(max_length=80)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Scorekeeper',
            fields=[
                ('name', models.CharField(max_length=80)),
                ('phoneNumber', models.CharField(max_length=80)),
                ('email', models.CharField(max_length=80)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Season',
            fields=[
                ('name', models.CharField(max_length=50)),
                ('startDate', models.DateField(blank=True, null=True)),
                ('endDate', models.DateField(blank=True, null=True)),
                ('numGames', models.CharField(max_length=3)),
                ('seasonActive', models.BooleanField(default=False)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('name', models.CharField(max_length=80)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('division', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.division')),
            ],
        ),
        migrations.CreateModel(
            name='TeamStats',
            fields=[
                ('regWins', models.IntegerField(default=0)),
                ('regLoses', models.IntegerField(default=0)),
                ('otWins', models.IntegerField(default=0)),
                ('otLoses', models.IntegerField(default=0)),
                ('ties', models.IntegerField(default=0)),
                ('points', models.IntegerField(default=0)),
                ('goalsFor', models.IntegerField(default=0)),
                ('goalsAgainst', models.IntegerField(default=0)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('team', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='home.team')),
            ],
        ),
        migrations.CreateModel(
            name='PlayerStats',
            fields=[
                ('goals', models.IntegerField(default=0)),
                ('assists', models.IntegerField(default=0)),
                ('points', models.IntegerField(default=0)),
                ('penaltyMins', models.IntegerField(default=0)),
                ('gamesPlayed', models.IntegerField(default=0)),
                ('playoffEligible', models.BooleanField(default=False)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('player', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='home.player')),
            ],
        ),
        migrations.AddField(
            model_name='player',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.team'),
        ),
        migrations.CreateModel(
            name='Penalty',
            fields=[
                ('period', models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('OT', 'OT')], max_length=100)),
                ('severity', models.CharField(choices=[('Minor', 'Minor'), ('Double Minor', 'Double Minor'), ('Major', 'Major'), ('Game Misconduct', 'Game Misconduct'), ('Match', 'Match')], max_length=100)),
                ('length', models.CharField(choices=[('2', '2'), ('4', '4'), ('5', '5'), ('10', '10')], max_length=100)),
                ('type', models.CharField(choices=[('Charging', 'Charging'), ('Cross-checking', 'Cross-checking'), ('Delay of game', 'Delay of game'), ('Elbowing', 'Elbowing'), ('Embellishment', 'Embellishment'), ('Goaltender interference', 'Goaltender interference'), ('High-sticking', 'High-sticking'), ('Hooking', 'Hooking'), ('Interference', 'Interference'), ('Roughing', 'Roughing'), ('Slashing', 'Slashing'), ('Tripping', 'Tripping'), ('Unsportsmanlike conduct', 'Unsportsmanlike conduct'), ('Too many men on the ice', 'Too many men on the ice'), ('Boarding', 'Boarding'), ('Fighting', 'Fighting')], max_length=100)),
                ('timeCommitted', models.CharField(max_length=80)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.game')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.player')),
            ],
        ),
        migrations.CreateModel(
            name='IceSlot',
            fields=[
                ('date', models.DateField(blank=True, null=True)),
                ('time', models.TimeField(blank=True, null=True)),
                ('available', models.BooleanField(default=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('rink', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.rink')),
            ],
        ),
        migrations.CreateModel(
            name='Goal',
            fields=[
                ('period', models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('OT', 'OT')], max_length=100)),
                ('timeScored', models.CharField(max_length=80)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('assistPrimary', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Primary_Assist', to='home.player')),
                ('assistSecondary', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Secondary_Assist', to='home.player')),
                ('goalScorer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Goal_Scorer', to='home.player')),
            ],
        ),
        migrations.CreateModel(
            name='GameResult',
            fields=[
                ('winType', models.CharField(choices=[('Regulation', 'REG'), ('Overtime', 'OT'), ('Shootout', 'SO'), ('Tie', 'TIE')], max_length=100)),
                ('winnerScore', models.IntegerField()),
                ('loserScore', models.IntegerField()),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('game', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='home.game')),
                ('losingTeam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Losing_Team', to='home.team')),
                ('winningTeam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Winning_Team', to='home.team')),
            ],
        ),
        migrations.AddField(
            model_name='game',
            name='awayTeam',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Away_Team', to='home.team'),
        ),
        migrations.AddField(
            model_name='game',
            name='homeTeam',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Home_Team', to='home.team'),
        ),
        migrations.AddField(
            model_name='game',
            name='iceSlot',
            field=models.OneToOneField(limit_choices_to={'available': True}, on_delete=django.db.models.deletion.CASCADE, to='home.iceslot'),
        ),
        migrations.AddField(
            model_name='game',
            name='referees',
            field=models.ManyToManyField(blank=True, to='home.Referee'),
        ),
        migrations.AddField(
            model_name='game',
            name='scorekeeper',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='home.scorekeeper'),
        ),
        migrations.AddField(
            model_name='division',
            name='season',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.season'),
        ),
    ]
